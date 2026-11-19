from django.shortcuts import render, get_object_or_404

from ..decorators import student_required
from ..models import Profile


@student_required
def student_profile(request):

    profile = get_object_or_404(
        Profile.objects.select_related('user'),
        user=request.user,
        role='student'
    )

    context = {
        'profile': profile,
        'user': request.user,
    }

    return render(request, 'student_profile.html', context)

from django.shortcuts import render
from ..decorators import teacher_required


@teacher_required
def teacher_profile(request):

    profile = request.user.profile

    context = {
        'user': request.user,
        'profile': profile,
    }

    return render(request, 'teacher_profile.html', context)