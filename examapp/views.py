from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .decorators import student_required


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
