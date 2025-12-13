from django.contrib import admin
from .models import VitalPoint, LearningHistory, QuizSession, SessionQuestion


@admin.register(VitalPoint)
class VitalPointAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'reading', 'category', 'image_file']
    list_filter = ['category']
    search_fields = ['name', 'reading', 'number']


@admin.register(LearningHistory)
class LearningHistoryAdmin(admin.ModelAdmin):
    list_display = ['vital_point', 'correct_count', 'incorrect_count', 'last_learned_at']
    list_filter = ['last_learned_at']
    search_fields = ['vital_point__name']


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'started_at', 'completed_at', 'current_question_index']
    list_filter = ['status', 'started_at']


@admin.register(SessionQuestion)
class SessionQuestionAdmin(admin.ModelAdmin):
    list_display = ['session', 'vital_point', 'question_order', 'is_answered', 'is_correct', 'attempt_count']
    list_filter = ['is_answered', 'is_correct']
    search_fields = ['vital_point__name']
