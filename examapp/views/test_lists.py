from django.shortcuts import render

from ..decorators import student_required
from ..models import TestAttempt
from ..services import (
    apply_search_filters,
    finalize_expired_attempts,
    get_available_tests,
)


@student_required
def available_tests(request):

    finalize_expired_attempts(request.user)

    tests = get_available_tests(request.user).select_related(
        'teacher'
    ).order_by('start_time')

    tests = apply_search_filters(
        tests, request, title_field='title', subject_field='subject'
    )

    return render(request, 'available_tests.html', {'tests': tests})


@student_required
def in_progress_tests(request):

    finalize_expired_attempts(request.user)

    attempts = TestAttempt.objects.filter(
        student=request.user,
        status='in_progress'
    ).select_related('test').order_by('-started_at')

    attempts = apply_search_filters(
        attempts, request, title_field='test__title', subject_field='test__subject'
    )

    return render(request, 'in_progress_tests.html', {'attempts': attempts})


@student_required
def completed_tests(request):

    attempts = TestAttempt.objects.filter(
        student=request.user,
        status='completed'
    ).select_related('test').order_by('-submitted_at')

    attempts = apply_search_filters(
        attempts, request, title_field='test__title', subject_field='test__subject'
    )

    return render(request, 'completed_tests.html', {'attempts': attempts})
