import random
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import VitalPoint, LearningHistory, QuizSession, SessionQuestion
from .serializers import (
    VitalPointSerializer, LearningHistorySerializer,
    QuizSessionSerializer, AnswerSubmitSerializer
)


class VitalPointViewSet(viewsets.ReadOnlyModelViewSet):
    """急所マスターデータのAPI"""
    queryset = VitalPoint.objects.all()
    serializer_class = VitalPointSerializer


class LearningHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """学習履歴のAPI"""
    queryset = LearningHistory.objects.select_related('vital_point').all()
    serializer_class = LearningHistorySerializer

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """統計情報を取得"""
        # get_queryset()を使って最新のデータを取得
        histories = self.get_queryset()
        total_correct = sum(h.correct_count for h in histories)
        total_incorrect = sum(h.incorrect_count for h in histories)
        total_attempts = total_correct + total_incorrect

        return Response({
            'total_correct': total_correct,
            'total_incorrect': total_incorrect,
            'total_attempts': total_attempts,
            'accuracy_rate': (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        })

    @action(detail=False, methods=['get'])
    def weak_points(self, request):
        """苦手な急所を取得（不正解が多い順）"""
        weak_histories = self.get_queryset().filter(
            incorrect_count__gt=0
        ).order_by('-incorrect_count')[:10]

        serializer = self.get_serializer(weak_histories, many=True)
        return Response(serializer.data)


class QuizSessionViewSet(viewsets.ModelViewSet):
    """クイズセッションのAPI"""
    queryset = QuizSession.objects.prefetch_related('questions__vital_point').all()
    serializer_class = QuizSessionSerializer

    @action(detail=False, methods=['post'])
    def start_new_session(self, request):
        """新規セッションを開始"""
        # 新しいセッションを作成
        session = QuizSession.objects.create()

        # 不正解が多い順モードかどうかを確認
        weak_points_mode = request.data.get('weak_points_mode', False)

        if weak_points_mode:
            # 不正解が多い順に取得（学習履歴がない場合はランダム）
            histories = LearningHistory.objects.select_related('vital_point').filter(
                incorrect_count__gt=0
            ).order_by('-incorrect_count')

            # 不正解のある急所を優先的に配置
            weak_points = [h.vital_point for h in histories]

            # まだ学習していない、または不正解が0の急所を取得
            weak_point_ids = [vp.id for vp in weak_points]
            remaining_points = list(VitalPoint.objects.exclude(id__in=weak_point_ids))
            random.shuffle(remaining_points)

            # 不正解が多い順 + 残りをランダム順で結合
            all_vital_points = weak_points + remaining_points
        else:
            # 全急所をランダム順で取得
            all_vital_points = list(VitalPoint.objects.all())
            random.shuffle(all_vital_points)

        # セッション問題を作成
        for order, vital_point in enumerate(all_vital_points, start=1):
            SessionQuestion.objects.create(
                session=session,
                vital_point=vital_point,
                question_order=order
            )

        serializer = self.get_serializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def current_question(self, request, pk=None):
        """現在の問題を取得"""
        session = self.get_object()

        # 未回答の問題を取得
        current_question = session.questions.filter(
            is_answered=False
        ).order_by('question_order').first()

        if not current_question:
            return Response({'message': '全ての問題に回答済みです'}, status=status.HTTP_200_OK)

        # 選択肢を生成（正解 + ランダムな不正解3つ）
        correct_answer = current_question.vital_point
        # 正解のIDと名前が同じものを除外（重複する名前がある場合に対応）
        other_points = list(VitalPoint.objects.exclude(id=correct_answer.id).exclude(name=correct_answer.name))
        random.shuffle(other_points)
        wrong_answers = other_points[:3]

        choices = [correct_answer] + wrong_answers
        random.shuffle(choices)

        return Response({
            'question_id': current_question.id,
            'question_order': current_question.question_order,
            'image_file': correct_answer.image_file,
            'number': correct_answer.number,
            'choices': [{'id': vp.id, 'name': vp.name, 'reading': vp.reading} for vp in choices],
            'total_questions': session.questions.count(),
            'answered_count': session.questions.filter(is_answered=True).count()
        })

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        """回答を送信"""
        session = self.get_object()
        serializer = AnswerSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question_id = serializer.validated_data['question_id']
        selected_answer = serializer.validated_data['selected_answer']

        try:
            question = session.questions.get(id=question_id)
        except SessionQuestion.DoesNotExist:
            return Response(
                {'error': '問題が見つかりません'},
                status=status.HTTP_404_NOT_FOUND
            )

        correct_answer = question.vital_point.name
        is_correct = selected_answer == correct_answer

        # 試行回数を増やす
        question.attempt_count += 1

        if is_correct:
            # 正解の場合
            question.is_answered = True
            question.is_correct = True
            question.save()

            # 学習履歴を更新
            history, created = LearningHistory.objects.get_or_create(
                vital_point=question.vital_point
            )
            history.correct_count += 1
            history.last_learned_at = timezone.now()
            history.save()

            return Response({
                'is_correct': True,
                'message': '正解です！',
                'correct_answer': correct_answer
            })
        else:
            # 不正解の場合
            question.save()

            # 学習履歴を更新
            history, created = LearningHistory.objects.get_or_create(
                vital_point=question.vital_point
            )
            history.incorrect_count += 1
            history.last_learned_at = timezone.now()
            history.save()

            return Response({
                'is_correct': False,
                'message': '不正解です。もう一度挑戦してください。',
                'correct_answer': correct_answer
            })

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        """セッションを中断"""
        session = self.get_object()
        session.status = 'paused'
        session.save()
        return Response({'message': 'セッションを中断しました'})

    @action(detail=True, methods=['post'])
    def resume(self, request, pk=None):
        """セッションを再開"""
        session = self.get_object()
        session.status = 'active'
        session.save()
        return Response({'message': 'セッションを再開しました'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """セッションを完了"""
        session = self.get_object()
        session.status = 'completed'
        session.completed_at = timezone.now()
        session.save()
        return Response({'message': 'セッションが完了しました'})
