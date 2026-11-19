from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Max, Count

from ..decorators import teacher_required
from ..models import Test, TestAttempt, AttemptAnswer


@teacher_required
def teacher_test_attempts(request, test_id):

    test = get_object_or_404(
        Test,
        id=test_id,
        teacher=request.user
    )

    attempts = TestAttempt.objects.filter(
        test=test
    ).select_related('student').order_by('-started_at')

    context = {
        'test': test,
        'attempts': attempts,
    }

    return render(
        request,
        'teacher_test_attempts.html',
        context
    )

@teacher_required
def teacher_attempt_detail(request, attempt_id):

    attempt = get_object_or_404(
        TestAttempt.objects.select_related('test', 'student'),
        id=attempt_id,
        test__teacher=request.user
    )

    answers = AttemptAnswer.objects.filter(
        test_attempt=attempt
    ).select_related('question')

    context = {
        'attempt': attempt,
        'answers': answers,
    }

    return render(
        request,
        'teacher_attempt_detail.html',
        context
    )

@teacher_required
def teacher_test_performance(request, test_id):

    test = get_object_or_404(
        Test,
        id=test_id,
        teacher=request.user
    )

    attempts = TestAttempt.objects.filter(test=test)

    completed_attempts = attempts.filter(status='completed')

    total_attempts = attempts.count()
    completed_count = completed_attempts.count()
    in_progress_count = attempts.filter(status='in_progress').count()

    performance = completed_attempts.aggregate(
        average_marks=Avg('marks_obtained'),
        highest_marks=Max('marks_obtained')
    )

    context = {
        'test': test,
        'total_attempts': total_attempts,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'average_marks': performance['average_marks'] or 0,
        'highest_marks': performance['highest_marks'] or 0,
    }

    return render(
        request,
        'teacher_test_performance.html',
        context
    )