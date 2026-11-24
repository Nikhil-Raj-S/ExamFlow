from datetime import timedelta
import logging
from django.db.models import Exists, OuterRef, Q
from django.utils import timezone

from .models import Test, TestAttempt, AttemptAnswer
from django.conf import settings
from django.core.mail import send_mail


# ---------- Attempt timing ----------

def attempt_end_time(attempt):
    return attempt.started_at + timedelta(minutes=attempt.test.duration_minutes)


def is_attempt_expired(attempt, now=None):
    """True if the time limit is over or the test's submission date has passed."""
    now = now or timezone.now()
    return (
        now >= attempt_end_time(attempt)
        or attempt.test.last_date_for_submission < timezone.localdate()
    )


# ---------- Finalizing attempts ----------

def finalize_attempt(attempt):
    if attempt.status == 'completed':
        return

    answers = AttemptAnswer.objects.filter(
        test_attempt=attempt
    ).select_related('question')

    total_marks = 0

    for answer in answers:
        if answer.selected_option == answer.question.correct_option:
            answer.marks_obtained = 1
        else:
            answer.marks_obtained = 0
        total_marks += answer.marks_obtained

    AttemptAnswer.objects.bulk_update(answers, ['marks_obtained'])

    attempt.marks_obtained = total_marks
    attempt.status = 'completed'
    attempt.submitted_at = timezone.now()
    attempt.save(update_fields=['marks_obtained', 'status', 'submitted_at'])


def finalize_expired_attempts(student):
    attempts = TestAttempt.objects.filter(
        student=student,
        status='in_progress'
    ).select_related('test')

    now = timezone.now()

    for attempt in attempts:
        if is_attempt_expired(attempt, now):
            finalize_attempt(attempt)


# ---------- Querysets ----------

def get_available_tests(student):
    """Published, currently open tests the student has no active attempt on."""
    now = timezone.now()

    active_attempts = TestAttempt.objects.filter(
        student=student,
        test_id=OuterRef('pk'),
        status='in_progress'
    )

    return Test.objects.filter(
        start_time__lte=now,
        last_date_for_submission__gte=timezone.localdate(),
        is_published=True
    ).annotate(
        has_active_attempt=Exists(active_attempts)
    ).filter(
        has_active_attempt=False
    )


def apply_search_filters(queryset, request, title_field, subject_field):
    """Applies ?search= and ?subject= from the request to any queryset."""
    search = request.GET.get('search', '').strip()
    subject = request.GET.get('subject', '').strip()

    if search:
        queryset = queryset.filter(Q(**{f'{title_field}__icontains': search}))

    if subject:
        queryset = queryset.filter(**{f'{subject_field}__iexact': subject})

    return queryset


#------------sending email------------

logger = logging.getLogger(__name__)

def send_test_result_email(attempt_id):

    try:
        attempt = TestAttempt.objects.select_related(
            'student', 'test'
        ).get(id=attempt_id)

        student_email = attempt.student.email

        if not student_email:
            logger.warning(
                "No email address found for student %s",
                attempt.student_id
            )
            return

        subject = f"Your test result: {attempt.test.title}"

        message = f"""
                Hello {attempt.student.first_name or attempt.student.username},

                Your test has been submitted successfully.

                Test: {attempt.test.title}
                Marks obtained: {attempt.marks_obtained}
                Total marks: {attempt.test.total_marks}

                Thank you for using ExamFlow.

                Best regards,
                ExamFlow Team
                """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student_email],
            fail_silently=False,
        )

    except Exception:
        logger.exception(
            "Failed to send result email for attempt %s",
            attempt_id
        )