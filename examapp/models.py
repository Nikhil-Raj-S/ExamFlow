from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Profile(models.Model):

    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    # Personal information
    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    # Public profile information
    headline = models.CharField(
        max_length=150,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        blank=True
    )

    linkedin_url = models.URLField(
        blank=True
    )

    website_url = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def age(self):
        if not self.date_of_birth:
            return None

        today = timezone.localdate()

        return (
            today.year - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class LearnerProfile(models.Model):

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='learner_details'
    )

    # Education
    highest_education = models.CharField(
        max_length=150,
        blank=True
    )

    institution = models.CharField(
        max_length=200,
        blank=True
    )

    field_of_study = models.CharField(
        max_length=150,
        blank=True
    )

    # Learning and career
    current_occupation = models.CharField(
        max_length=150,
        blank=True
    )

    skills = models.TextField(
        blank=True
    )

    interests = models.TextField(
        blank=True
    )

    learning_goals = models.TextField(
        blank=True
    )

    career_goals = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"Learner: {self.profile.user.username}"


class InstructorProfile(models.Model):

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='instructor_details'
    )

    # Professional information
    qualification = models.CharField(
        max_length=200,
        blank=True
    )

    organization = models.CharField(
        max_length=200,
        blank=True
    )

    designation = models.CharField(
        max_length=150,
        blank=True
    )

    years_of_experience = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(60)]
    )

    # Expertise and teaching
    expertise = models.TextField(
        blank=True
    )

    certifications = models.TextField(
        blank=True
    )

    professional_background = models.TextField(
        blank=True
    )

    teaching_experience = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"Instructor: {self.profile.user.username}"


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

    option_a = models.CharField(max_length=255)

    option_b = models.CharField(max_length=255)

    option_c = models.CharField(max_length=255)

    option_d = models.CharField(max_length=255)

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
        models.UniqueConstraint(
            fields=['student', 'test'],
            condition=models.Q(status='in_progress'),
            name='unique_active_attempt_per_student_test',
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