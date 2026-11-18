from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import HttpResponseForbidden


def student_required(view_func):

    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.profile.role != 'student':
            return HttpResponseForbidden('Access Denied')

        return view_func(request, *args, **kwargs)

    return wrapper


def teacher_required(view_func):

    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.profile.role != 'teacher':
            return HttpResponseForbidden('Access Denied')

        return view_func(request, *args, **kwargs)

    return wrapper
