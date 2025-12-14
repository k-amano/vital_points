from django.db import models


class VitalPoint(models.Model):
    """急所マスターデータ"""
    number = models.CharField(max_length=10, verbose_name="番号")
    name = models.CharField(max_length=50, verbose_name="急所名")
    reading = models.CharField(max_length=50, verbose_name="読み仮名")
    category = models.CharField(max_length=100, verbose_name="カテゴリ")
    image_file = models.CharField(max_length=255, verbose_name="画像ファイル名")

    class Meta:
        verbose_name = "急所"
        verbose_name_plural = "急所一覧"
        ordering = ['id']

    def __str__(self):
        return f"{self.number} {self.name} ({self.reading})"


class LearningHistory(models.Model):
    """学習履歴データ"""
    vital_point = models.OneToOneField(
        VitalPoint,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name="急所"
    )
    correct_count = models.IntegerField(default=0, verbose_name="正解回数")
    incorrect_count = models.IntegerField(default=0, verbose_name="不正解回数")
    last_learned_at = models.DateTimeField(null=True, blank=True, verbose_name="最終学習日時")

    class Meta:
        verbose_name = "学習履歴"
        verbose_name_plural = "学習履歴一覧"

    def __str__(self):
        return f"{self.vital_point.name} - 正解:{self.correct_count} 不正解:{self.incorrect_count}"

    @property
    def accuracy_rate(self):
        """正解率を計算"""
        total = self.correct_count + self.incorrect_count
        if total == 0:
            return 0
        return (self.correct_count / total) * 100


class QuizSession(models.Model):
    """クイズセッションデータ"""
    STATUS_CHOICES = [
        ('active', '進行中'),
        ('paused', '中断'),
        ('completed', '完了'),
    ]

    MODE_CHOICES = [
        ('test', 'テスト'),
        ('review', '復習'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="ステータス"
    )
    mode = models.CharField(
        max_length=20,
        choices=MODE_CHOICES,
        default='test',
        verbose_name="モード"
    )
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="開始日時")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="完了日時")
    current_question_index = models.IntegerField(default=0, verbose_name="現在の問題番号")

    class Meta:
        verbose_name = "クイズセッション"
        verbose_name_plural = "クイズセッション一覧"
        ordering = ['-started_at']

    def __str__(self):
        return f"セッション {self.id} - {self.get_mode_display()} - {self.get_status_display()}"


class SessionQuestion(models.Model):
    """セッション内の問題データ"""
    session = models.ForeignKey(
        QuizSession,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="セッション"
    )
    vital_point = models.ForeignKey(
        VitalPoint,
        on_delete=models.CASCADE,
        verbose_name="急所"
    )
    question_order = models.IntegerField(verbose_name="出題順")
    is_answered = models.BooleanField(default=False, verbose_name="回答済み")
    is_correct = models.BooleanField(default=False, verbose_name="正解")
    attempt_count = models.IntegerField(default=0, verbose_name="試行回数")

    class Meta:
        verbose_name = "セッション問題"
        verbose_name_plural = "セッション問題一覧"
        ordering = ['question_order']
        unique_together = ['session', 'question_order']

    def __str__(self):
        return f"{self.session.id} - Q{self.question_order}: {self.vital_point.name}"


class TestResult(models.Model):
    """テスト結果データ（テストモードのみ）"""
    session = models.OneToOneField(
        QuizSession,
        on_delete=models.CASCADE,
        related_name='test_result',
        verbose_name="セッション"
    )
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="完了日時")
    total_questions = models.IntegerField(verbose_name="総問題数")
    correct_count = models.IntegerField(verbose_name="正解数")
    incorrect_count = models.IntegerField(verbose_name="不正解数")
    score = models.IntegerField(verbose_name="得点")

    class Meta:
        verbose_name = "テスト結果"
        verbose_name_plural = "テスト結果一覧"
        ordering = ['-completed_at']

    def __str__(self):
        return f"テスト結果 {self.id} - {self.score}点 ({self.correct_count}/{self.total_questions})"
