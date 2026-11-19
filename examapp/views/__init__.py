# Re-export everything so urls.py (`from . import views` / `views.xyz`) keeps working.
from .auth import user_login, user_logout
from .dashboard import student_dashboard
from .test_lists import available_tests, in_progress_tests, completed_tests
from .attempts import (
    test_detail,
    start_test,
    take_test,
    save_answer,
    submit_test,
    test_result,
)
from .profile import student_profile
