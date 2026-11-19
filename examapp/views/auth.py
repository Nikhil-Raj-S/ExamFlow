from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from ..models import Profile


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            profile = Profile.objects.filter(user=user).first()

            if profile is None:
                messages.error(request, 'Your profile is not configured.')
                return render(request, 'login.html')

            if profile.role == 'student':
                login(request, user)
                return redirect('StudentDashboard')

            elif profile.role == 'teacher':
                login(request, user)
                return redirect('TeacherDashboard')

            messages.error(request, 'Invalid account role.')

        else:
            messages.error(request, 'Incorrect username or password.')

    return render(request, 'login.html')


@login_required
@require_POST
def user_logout(request):

    logout(request)

    return redirect('Login')
