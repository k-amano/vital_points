import random
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import VitalPoint, LearningHistory, QuizSession, SessionQuestion, TestResult
from .serializers import (
    VitalPointSerializer, LearningHistorySerializer,
    QuizSessionSerializer, QuizSessionSummarySerializer,
    TestResultSerializer, AnswerSubmitSerializer
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
        """統計情報を取得（テスト結果のみ）"""
        # テスト結果から集計
        test_results = TestResult.objects.all()
        total_correct = sum(r.correct_count for r in test_results)
        total_incorrect = sum(r.incorrect_count for r in test_results)
        total_attempts = total_correct + total_incorrect

        return Response({
            'total_correct': total_correct,
            'total_incorrect': total_incorrect,
            'total_attempts': total_attempts,
            'accuracy_rate': (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        })

    @action(detail=False, methods=['get'])
    def weak_points(self, request):
        """苦手な急所を取得（不正解率が高い順、上位10件）"""
        histories = list(self.get_queryset().filter(
            incorrect_count__gt=0
        ))

        # 不正解率でソート
        histories.sort(
            key=lambda h: h.incorrect_count / (h.correct_count + h.incorrect_count),
            reverse=True
        )

        # 上位10件
        weak_histories = histories[:10]

        serializer = self.get_serializer(weak_histories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def test_results(self, request):
        """テスト結果一覧（最新10件）"""
        results = TestResult.objects.all().order_by('-completed_at')[:10]
        serializer = TestResultSerializer(results, many=True)
        return Response(serializer.data)


class QuizSessionViewSet(viewsets.ModelViewSet):
    """クイズセッションのAPI"""
    queryset = QuizSession.objects.prefetch_related('questions__vital_point').all()
    serializer_class = QuizSessionSerializer

    @action(detail=False, methods=['post'])
    def start_new_session(self, request):
        """新規セッションを開始"""
        # モードを取得（test または review）
        mode = request.data.get('mode', 'test')

        # 新しいセッションを作成
        session = QuizSession.objects.create(mode=mode)

        if mode == 'review':
            # 復習モード: 不正解率が高い順に25題
            histories = list(LearningHistory.objects.select_related('vital_point').filter(
                incorrect_count__gt=0
            ))

            # 不正解率でソート（降順）
            histories.sort(
                key=lambda h: h.incorrect_count / (h.correct_count + h.incorrect_count),
                reverse=True
            )

            # 不正解率が高い順に最大10題
            selected_points = [h.vital_point for h in histories[:10]]

            # 不正解のある問題がない場合は終了
            if len(selected_points) == 0:
                session.delete()
                return Response(
                    {'message': '復習する問題がありません'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # テストモード: ランダムに25題
            all_vital_points = list(VitalPoint.objects.all())
            random.shuffle(all_vital_points)
            selected_points = all_vital_points[:25]

        # セッション問題を作成（テスト: 25題、復習: 10題）
        for order, vital_point in enumerate(selected_points, start=1):
            SessionQuestion.objects.create(
                session=session,
                vital_point=vital_point,
                question_order=order
            )

        # 軽量版のシリアライザーを使用
        serializer = QuizSessionSummarySerializer(session)
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

        # 回答を記録（正解・不正解に関わらず完了扱い）
        question.is_answered = True
        question.is_correct = is_correct
        question.save()

        # 学習履歴を更新
        history, created = LearningHistory.objects.get_or_create(
            vital_point=question.vital_point
        )

        if is_correct:
            history.correct_count += 1
        else:
            history.incorrect_count += 1

        history.last_learned_at = timezone.now()
        history.save()

        return Response({
            'is_correct': is_correct,
            'message': '正解です！' if is_correct else f'不正解です。正解は「{correct_answer}」です。',
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

        # 結果を計算
        total_questions = session.questions.count()
        correct_count = session.questions.filter(is_correct=True).count()
        incorrect_count = total_questions - correct_count
        score = int((correct_count / total_questions) * 100) if total_questions > 0 else 0

        # テストモードの場合、TestResultを作成
        if session.mode == 'test':
            TestResult.objects.create(
                session=session,
                total_questions=total_questions,
                correct_count=correct_count,
                incorrect_count=incorrect_count,
                score=score
            )

        return Response({
            'message': 'セッションが完了しました',
            'mode': session.mode,
            'total_questions': total_questions,
            'correct_count': correct_count,
            'incorrect_count': incorrect_count,
            'score': score
        })
