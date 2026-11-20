
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from ..decorators import student_required, teacher_required
from ..models import Profile, LearnerProfile, InstructorProfile
from ..forms import (
    ProfileForm,
    LearnerProfileForm,
    InstructorProfileForm,
)


@student_required
def student_profile(request):
    profile = get_object_or_404(
        Profile.objects.select_related('user'),
        user=request.user,
        role='student'
    )

    role_profile, _ = LearnerProfile.objects.get_or_create(
        profile=profile
    )

    return render(
        request,
        'student_profile.html',
        {
            'profile': profile,
            'user': request.user,
            'role_profile': role_profile,
        }
    )


@teacher_required
def teacher_profile(request):
    profile = get_object_or_404(
        Profile.objects.select_related('user'),
        user=request.user,
        role='teacher'
    )

    role_profile, _ = InstructorProfile.objects.get_or_create(
        profile=profile
    )

    return render(
        request,
        'teacher_profile.html',
        {
            'profile': profile,
            'user': request.user,
            'role_profile': role_profile,
        }
    )


@login_required
def edit_profile(request):

    with transaction.atomic():

        profile = get_object_or_404(
            Profile.objects.select_for_update(),
            user=request.user
        )

        if profile.role == 'student':
            role_profile, _ = LearnerProfile.objects.get_or_create(
                profile=profile
            )
            RoleForm = LearnerProfileForm

        elif profile.role == 'teacher':
            role_profile, _ = InstructorProfile.objects.get_or_create(
                profile=profile
            )
            RoleForm = InstructorProfileForm

        else:
            messages.error(request, 'Invalid profile role.')
            return redirect('Login')

        if request.method == 'POST':

            profile_form = ProfileForm(
                request.POST,
                request.FILES,
                instance=profile,
                user=request.user,
            )

            role_form = RoleForm(
                request.POST,
                instance=role_profile
            )

            if profile_form.is_valid() and role_form.is_valid():

                profile_form.save()

                request.user.email = profile_form.cleaned_data['email']
                request.user.save(update_fields=['email'])

                role_form.save()

                messages.success(
                    request,
                    'Your profile has been updated successfully.'
                )

                if profile.role == 'student':
                    return redirect('StudentProfile')

                return redirect('TeacherProfile')

        else:

            profile_form = ProfileForm(
                instance=profile,
                user=request.user,
            )

            role_form = RoleForm(
                instance=role_profile
            )

    return render(
        request,
        'edit_profile.html',
        {
            'profile': profile,
            'profile_form': profile_form,
            'role_form': role_form,
        }
    )
