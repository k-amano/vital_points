from rest_framework import serializers
from .models import VitalPoint, LearningHistory, QuizSession, SessionQuestion


class VitalPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalPoint
        fields = ['id', 'number', 'name', 'reading', 'category', 'image_file']


class LearningHistorySerializer(serializers.ModelSerializer):
    vital_point = VitalPointSerializer(read_only=True)
    accuracy_rate = serializers.ReadOnlyField()

    class Meta:
        model = LearningHistory
        fields = ['id', 'vital_point', 'correct_count', 'incorrect_count',
                  'last_learned_at', 'accuracy_rate']


class SessionQuestionSerializer(serializers.ModelSerializer):
    vital_point = VitalPointSerializer(read_only=True)

    class Meta:
        model = SessionQuestion
        fields = ['id', 'vital_point', 'question_order', 'is_answered',
                  'is_correct', 'attempt_count']


class QuizSessionSerializer(serializers.ModelSerializer):
    questions = SessionQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = QuizSession
        fields = ['id', 'status', 'started_at', 'completed_at',
                  'current_question_index', 'questions']


class QuizSessionSummarySerializer(serializers.ModelSerializer):
    """セッション作成時など、質問データを含まない軽量版"""
    class Meta:
        model = QuizSession
        fields = ['id', 'status', 'started_at', 'completed_at',
                  'current_question_index']


class AnswerSubmitSerializer(serializers.Serializer):
    """回答送信用シリアライザー"""
    session_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    selected_answer = serializers.CharField()
