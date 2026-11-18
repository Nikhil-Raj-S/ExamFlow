from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):

    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
    )

    role = models.CharField(
        max_length = 10,
        choices = ROLE_CHOICES,
    )

    def __str__(self):

        return f"{self.user.username} - {self.role}"


class Test(models.Model):

    teacher = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )

    title = models.CharField(max_length = 20)

    created_at = models.DateTimeField(auto_now_add=True)

    start_time = models.DateTimeField(null=True,blank=True)

    duration_minutes = models.PositiveIntegerField(validators = [
        MinValueValidator(1), MaxValueValidator(120) ])

    subject = models.CharField(max_length = 20)

    total_marks = models.PositiveIntegerField()

    last_date_for_submission = models.DateField()

    is_published = models.BooleanField(default = False)


class Question(models.Model):

    choices = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    test = models.ForeignKey(
        Test,
        on_delete = models.CASCADE
    )

    question_text = models.TextField()

    option_a = models.CharField()

    option_b = models.CharField()

    option_c = models.CharField()

    option_d = models.CharField()

    correct_option = models.CharField(
    max_length = 1,
    choices = choices,
)

class TestAttempt(models.Model):

    status_choices = [
        ('completed', 'Completed'),
        ('in_progress', 'InProgress'),
    ]

    student = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )

    test = models.ForeignKey(
        Test,
        on_delete = models.CASCADE,
    )

    marks_obtained = models.PositiveIntegerField(default=0)

    attempt_no = models.PositiveIntegerField()

    started_at = models.DateTimeField(auto_now_add=True)

    submitted_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length = 20, 
        choices = status_choices,
        default='in_progress',
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['student', 'test', 'attempt_no'],
                name = 'unique_student_test_and_attempt_no',
        ),
        ]


class AttemptAnswer(models.Model):

    choices = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]


    question = models.ForeignKey(
        Question,
        on_delete = models.CASCADE,
    )

    test_attempt = models.ForeignKey(
        TestAttempt,
        on_delete = models.CASCADE,
    )

    selected_option = models.CharField(
        max_length = 1,
        choices = choices,
    )

    marks_obtained = models.PositiveIntegerField(default = 0)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields = ['question', 'test_attempt'],
                name = 'unique_question_and_test_attempt',
            ),
        ]