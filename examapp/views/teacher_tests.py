from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from ..decorators import teacher_required
from ..models import Test, Question
from ..forms import TestCreationForm

@teacher_required
def create_test(request):

    if request.method == 'POST':

        form = TestCreationForm(request.POST)

        if form.is_valid():

            test = form.save(commit=False)
            test.teacher = request.user
            test.is_published = False
            test.save()

            messages.success(request, 'Test created successfully.')

            return redirect('TeacherDashboard')

    else:
        form = TestCreationForm()

    return render(request, 'create_test.html', {'form': form})


@teacher_required
def teacher_test_list(request):

    tests = Test.objects.filter(
        teacher=request.user
    ).order_by('-created_at')

    context = {
        'tests': tests
    }

    return render(request, 'teacher_test_list.html', context)


@teacher_required
def teacher_test_detail(request, test_id):

    test = get_object_or_404(
        Test,
        id=test_id,
        teacher=request.user
    )

    questions = Question.objects.filter(test=test)

    context = {
        'test': test,
        'questions': questions,
    }

    return render(request, 'teacher_test_detail.html', context)


@teacher_required
def edit_test(request, test_id):

    test = get_object_or_404(
        Test,
        id=test_id,
        teacher=request.user,
        is_published=False
    )

    if request.method == 'POST':
        form = TestCreationForm(request.POST, instance=test)

        if form.is_valid():
            form.save()
            messages.success(request, 'Test updated successfully.')
            return redirect('TeacherTestDetail', test_id=test.id)

    else:
        form = TestCreationForm(instance=test)

    return render(request, 'edit_test.html', {'form': form, 'test': test})

@teacher_required
@require_POST
def delete_test(request, test_id):

    test = get_object_or_404(
        Test,
        id=test_id,
        teacher=request.user,
        is_published=False
    )

    test.delete()

    messages.success(request, 'Test deleted successfully.')

    return redirect('TeacherTestList')

@teacher_required
@require_POST
def publish_test(request, test_id):
    test = get_object_or_404(
        Test,
        id=test_id,
        teacher=request.user,
        is_published=False
    )

    question_count = Question.objects.filter(test=test).count()

    if question_count == 0:
        messages.error(request, 'Add at least one question before publishing.')
        return redirect('TeacherTestDetail', test_id=test.id)

    test.is_published = True
    test.save(update_fields=['is_published'])

    messages.success(request, 'Test published successfully.')
    return redirect('TeacherTestDetail', test_id=test.id)