from django.db import transaction
from django.db.models import Max
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from ..decorators import student_required
from ..models import Test, TestAttempt, Question, AttemptAnswer
from ..services import (
    attempt_end_time,
    finalize_attempt,
    finalize_expired_attempts,
    is_attempt_expired,
)


@student_required
def test_detail(request, test_id):

    finalize_expired_attempts(request.user)

    test = get_object_or_404(Test, id=test_id, is_published=True)

    now = timezone.now()

    active_attempt = TestAttempt.objects.filter(
        student=request.user,
        test=test,
        status='in_progress'
    ).first()

    can_start = (
        test.start_time is not None
        and test.start_time <= now
        and test.last_date_for_submission >= timezone.localdate()
        and active_attempt is None
    )

    context = {
        'test': test,
        'active_attempt': active_attempt,
        'can_start': can_start,
    }

    return render(request, 'test_detail.html', context)


@student_required
@require_POST
def start_test(request, test_id):

    with transaction.atomic():

        test = get_object_or_404(
            Test.objects.select_for_update(),
            id=test_id,
            is_published=True
        )

        now = timezone.now()

        attempt = TestAttempt.objects.select_for_update().select_related(
            'test'
        ).filter(
            student=request.user,
            test=test,
            status='in_progress'
        ).first()

        if attempt:

            if is_attempt_expired(attempt, now):
                finalize_attempt(attempt)
                return redirect('TestResult', attempt_id=attempt.id)

            return redirect('TakeTest', attempt_id=attempt.id)

        if (
            test.start_time is None
            or test.start_time > now
            or test.last_date_for_submission < timezone.localdate()
        ):
            return HttpResponseForbidden('This test is not available.')

        last_attempt_no = TestAttempt.objects.filter(
            student=request.user,
            test=test
        ).aggregate(maximum=Max('attempt_no'))['maximum']

        attempt = TestAttempt.objects.create(
            student=request.user,
            test=test,
            attempt_no=(last_attempt_no or 0) + 1,
            status='in_progress'
        )

    return redirect('TakeTest', attempt_id=attempt.id)


@student_required
def take_test(request, attempt_id):

    with transaction.atomic():

        attempt = get_object_or_404(
            TestAttempt.objects.select_for_update().select_related('test'),
            id=attempt_id,
            student=request.user
        )

        if attempt.status == 'completed':
            return redirect('TestResult', attempt_id=attempt.id)

        if attempt.status != 'in_progress':
            return HttpResponseForbidden('Invalid attempt.')

        now = timezone.now()

        if is_attempt_expired(attempt, now):
            finalize_attempt(attempt)
            return redirect('TestResult', attempt_id=attempt.id)

        questions = Question.objects.filter(test=attempt.test).order_by('id')

        remaining_seconds = int((attempt_end_time(attempt) - now).total_seconds())

        context = {
            'attempt': attempt,
            'test': attempt.test,
            'questions': questions,
            'remaining_seconds': remaining_seconds,
        }

    return render(request, 'take_test.html', context)


@student_required
@require_POST
def save_answer(request, attempt_id):

    question_id = request.POST.get('question_id')
    selected_option = request.POST.get('selected_option')

    if not question_id or not selected_option:
        return HttpResponseBadRequest('Missing required data.')

    if selected_option not in {'A', 'B', 'C', 'D'}:
        return HttpResponseBadRequest('Invalid option.')

    try:
        question_id = int(question_id)
    except ValueError:
        return HttpResponseBadRequest('Invalid question ID.')

    with transaction.atomic():

        attempt = get_object_or_404(
            TestAttempt.objects.select_for_update().select_related('test'),
            id=attempt_id,
            student=request.user
        )

        if attempt.status == 'completed':
            return HttpResponseForbidden('Attempt already completed.')

        if attempt.status != 'in_progress':
            return HttpResponseForbidden('Invalid attempt.')

        if is_attempt_expired(attempt):
            finalize_attempt(attempt)
            return HttpResponseForbidden('Examination time has expired.')

        question = get_object_or_404(
            Question,
            id=question_id,
            test=attempt.test
        )

        AttemptAnswer.objects.update_or_create(
            test_attempt=attempt,
            question=question,
            defaults={'selected_option': selected_option}
        )

    return JsonResponse({'message': 'Answer saved successfully.'})


@student_required
@require_POST
def submit_test(request, attempt_id):

    with transaction.atomic():

        attempt = get_object_or_404(
            TestAttempt.objects.select_for_update().select_related('test'),
            id=attempt_id,
            student=request.user
        )

        if attempt.status == 'completed':
            return redirect('TestResult', attempt_id=attempt.id)

        if attempt.status != 'in_progress':
            return HttpResponseForbidden('Invalid attempt.')

        finalize_attempt(attempt)

    return redirect('TestResult', attempt_id=attempt.id)


@student_required
def test_result(request, attempt_id):

    attempt = get_object_or_404(
        TestAttempt.objects.select_related('test'),
        id=attempt_id,
        student=request.user,
        status='completed'
    )

    total_marks = attempt.test.total_marks

    percentage = (
        (attempt.marks_obtained / total_marks) * 100
        if total_marks > 0 else 0
    )

    context = {
        'attempt': attempt,
        'test': attempt.test,
        'total_marks': total_marks,
        'percentage': round(percentage, 2),
    }

    return render(request, 'test_result.html', context)
