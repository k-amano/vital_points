from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VitalPointViewSet, LearningHistoryViewSet, QuizSessionViewSet

router = DefaultRouter()
router.register(r'vital-points', VitalPointViewSet, basename='vital-point')
router.register(r'learning-history', LearningHistoryViewSet, basename='learning-history')
router.register(r'quiz-sessions', QuizSessionViewSet, basename='quiz-session')

urlpatterns = [
    path('', include(router.urls)),
]
