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

    path('teacher/tests/create/', views.create_test, name='CreateTest'),
    path('teacher/tests/', views.teacher_test_list, name='TeacherTestList'),
    path('teacher/tests/<int:test_id>/', views.teacher_test_detail, name='TeacherTestDetail'),
    path('teacher/tests/<int:test_id>/edit/', views.edit_test, name='EditTest'),
    path('teacher/tests/<int:test_id>/delete/', views.delete_test, name='DeleteTest'),

    path('teacher/tests/<int:test_id>/questions/create/', views.create_question, name='CreateQuestion'),
    path('teacher/questions/<int:question_id>/edit/', views.edit_question, name='EditQuestion'),
    path('teacher/questions/<int:question_id>/delete/', views.delete_question, name='DeleteQuestion'),
    path('teacher/tests/<int:test_id>/publish/', views.publish_test, name='PublishTest'),

    path('teacher/tests/<int:test_id>/attempts/', views.teacher_test_attempts, name='TeacherTestAttempts'),
    path('teacher/attempts/<int:attempt_id>/', views.teacher_attempt_detail, name='TeacherAttemptDetail'),
    path('teacher/tests/<int:test_id>/performance/', views.teacher_test_performance, name='TeacherTestPerformance'),

    path('teacher/profile/', views.teacher_profile, name='TeacherProfile'),
]