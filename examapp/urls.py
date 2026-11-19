from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='Login'),
    path('logout/', views.user_logout, name='Logout'),

    path('student/dashboard/', views.student_dashboard, name='StudentDashboard'),
    path('student/profile/', views.student_profile, name='StudentProfile'),

    path('student/tests/available/', views.available_tests, name='AvailableTests'),
    path('student/tests/in-progress/', views.in_progress_tests, name='InProgressTests'),
    path('student/tests/completed/', views.completed_tests, name='CompletedTests'),

    path('student/tests/<int:test_id>/', views.test_detail, name='TestDetail'),
    path('student/tests/<int:test_id>/start/', views.start_test, name='StartTest'),

    path('student/attempts/<int:attempt_id>/', views.take_test, name='TakeTest'),
    path('student/attempts/<int:attempt_id>/save/', views.save_answer, name='SaveAnswer'),
    path('student/attempts/<int:attempt_id>/submit/', views.submit_test, name='SubmitTest'),
    path('student/attempts/<int:attempt_id>/result/', views.test_result, name='TestResult'),
]