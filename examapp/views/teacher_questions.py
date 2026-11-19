from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..decorators import teacher_required
from ..models import Test
from ..forms import QuestionCreationForm
from django.views.decorators.http import require_POST


@teacher_required
def create_question(request, test_id):

    test = get_object_or_404(
        Test,
        id=test_id,
        teacher=request.user,
        is_published=False
    )

    if request.method == 'POST':
        form = QuestionCreationForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()

            messages.success(request, 'Question added successfully.')

            return redirect('TeacherTestDetail', test_id=test.id)

    else:
        form = QuestionCreationForm()

    return render(
        request,
        'create_question.html',
        {'form': form, 'test': test}
    )

@teacher_required
def edit_question(request, question_id):

    question = get_object_or_404(
        Question,
        id=question_id,
        test__teacher=request.user,
        test__is_published=False
    )

    if request.method == 'POST':
        form = QuestionCreationForm(request.POST, instance=question)

        if form.is_valid():
            form.save()

            messages.success(request, 'Question updated successfully.')

            return redirect(
                'TeacherTestDetail',
                test_id=question.test.id
            )

    else:
        form = QuestionCreationForm(instance=question)

    return render(
        request,
        'edit_question.html',
        {'form': form, 'question': question}
    )

@teacher_required
@require_POST
def delete_question(request, question_id):

    question = get_object_or_404(
        Question,
        id=question_id,
        test__teacher=request.user,
        test__is_published=False
    )

    test_id = question.test.id

    question.delete()

    messages.success(request, 'Question deleted successfully.')

    return redirect('TeacherTestDetail', test_id=test_id)