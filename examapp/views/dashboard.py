from django.db.models import F, Avg, FloatField, ExpressionWrapper
from django.shortcuts import render

from ..decorators import student_required
from ..models import TestAttempt
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
