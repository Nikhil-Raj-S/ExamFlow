from .auth import user_login, user_logout

from .dashboard import student_dashboard, teacher_dashboard

from .profile import student_profile, teacher_profile

from .test_lists import available_tests, in_progress_tests, completed_tests

from .attempts import test_detail, start_test, take_test, save_answer, submit_test, test_result

from .teacher_tests import create_test, teacher_test_list, teacher_test_detail, edit_test, delete_test, publish_test

from .teacher_questions import create_question, edit_question, delete_question

from .teacher_results import teacher_test_attempts, teacher_attempt_detail, teacher_test_performance