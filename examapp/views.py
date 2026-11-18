from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import F, Avg, FloatField, ExpressionWrapper, Exists, OuterRef
from django.utils import timezone

from .decorators import student_required
from .models import Test, TestAttempt

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username = username,
            password = password,
        )

        if user is not None:

            login(request,user)

            if user.profile.role == 'student':
                return redirect('StudentDashboard')
            if user.profile.role == 'teacher':
                return redirect('TeacherDashboard')

        else:

            messages.error(request, 'incorrect email or password')

    return render(request, 'login.html')



@student_required
def student_dashboard(request):

    now = timezone.now()

    # Check for an active attempt for each test
    attempts = TestAttempt.objects.filter(
        student=request.user,
        test_id=OuterRef('pk'),
        status='in_progress'
    )

    # Available tests queryset
    available_tests_queryset = Test.objects.filter(
        start_time__lte=now,
        last_date_for_submission__gte=now.date(),
        is_published=True
    ).annotate(
        has_active_attempt=Exists(attempts)
    ).filter(
        has_active_attempt=False
    )

    available_tests = available_tests_queryset.count()

    recent_available_tests = available_tests_queryset.order_by(
        'start_time'
    )[:3]

    # In-progress tests
    in_progress_queryset = TestAttempt.objects.filter(
        student=request.user,
        status='in_progress'
    )

    in_progress_tests = in_progress_queryset.count()

    recent_in_progress = in_progress_queryset.select_related(
        'test'
    ).order_by('-started_at')[:3]

    # Completed tests
    completed_queryset = TestAttempt.objects.filter(
        student=request.user,
        status='completed'
    )

    completed_tests = completed_queryset.count()

    recent_completed_tests = (
        completed_queryset
        .select_related('test')
        .order_by('-submitted_at')[:3]
    )

    # Average score
    average_score = completed_queryset.aggregate(
        average=Avg(
            ExpressionWrapper(
                F('marks_obtained') * 100.0 / F('test__total_marks'),
                output_field=FloatField()
            )
        )
    )['average']

    average_score = round(average_score, 2) if average_score is not None else 0

    context = {
        'available': available_tests,
        'in_progress': in_progress_tests,
        'completed': completed_tests,
        'average_score': average_score,
        'recent_in_progress': recent_in_progress,
        'recent_available_tests': recent_available_tests,
        'recent_completed_tests': recent_completed_tests,
    }

    return render(request, 'student_dashboard.html', context=context)
