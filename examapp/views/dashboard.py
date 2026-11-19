from django.db.models import F, Avg, FloatField, ExpressionWrapper
from django.shortcuts import render

from ..decorators import student_required, teacher_required
from ..models import TestAttempt, Test
from ..services import finalize_expired_attempts, get_available_tests


@student_required
def student_dashboard(request):

    finalize_expired_attempts(request.user)

    available_queryset = get_available_tests(request.user)

    in_progress_queryset = TestAttempt.objects.filter(
        student=request.user,
        status='in_progress'
    )

    completed_queryset = TestAttempt.objects.filter(
        student=request.user,
        status='completed'
    )

    average_score = completed_queryset.aggregate(
        average=Avg(
            ExpressionWrapper(
                F('marks_obtained') * 100.0 / F('test__total_marks'),
                output_field=FloatField()
            )
        )
    )['average']

    context = {
        'available': available_queryset.count(),
        'in_progress': in_progress_queryset.count(),
        'completed': completed_queryset.count(),
        'average_score': round(average_score, 2) if average_score is not None else 0,
        'recent_available_tests': available_queryset.order_by('start_time')[:3],
        'recent_in_progress': in_progress_queryset.select_related('test').order_by('-started_at')[:3],
        'recent_completed_tests': completed_queryset.select_related('test').order_by('-submitted_at')[:3],
    }

    return render(request, 'student_dashboard.html', context)

@teacher_required
def teacher_dashboard(request):

    # Get tests created by the logged-in teacher
    tests = Test.objects.filter(
        teacher=request.user
    )

    # Test statistics
    total_tests = tests.count()

    published_tests = tests.filter(
        is_published=True
    ).count()

    draft_tests = tests.filter(
        is_published=False
    ).count()

    # Student attempt statistics
    total_attempts = TestAttempt.objects.filter(
        test__teacher=request.user
    ).count()

    completed_attempts = TestAttempt.objects.filter(
        test__teacher=request.user,
        status='completed'
    ).count()

    in_progress_attempts = TestAttempt.objects.filter(
        test__teacher=request.user,
        status='in_progress'
    ).count()

    # Recently created tests
    recent_tests = tests.order_by('-created_at')[:5]

    context = {
        'total_tests': total_tests,
        'published_tests': published_tests,
        'draft_tests': draft_tests,
        'total_attempts': total_attempts,
        'completed_attempts': completed_attempts,
        'in_progress_attempts': in_progress_attempts,
        'recent_tests': recent_tests,
    }

    return render(
        request,
        'teacher_dashboard.html',
        context
    )
