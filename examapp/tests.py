from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Profile, Test, Question, TestAttempt


class AttemptFlowTests(TestCase):

    def setUp(self):
        teacher = User.objects.create_user('teacher1', password='pass12345')
        Profile.objects.create(user=teacher, role='teacher')

        self.student = User.objects.create_user('student1', password='pass12345')
        Profile.objects.create(user=self.student, role='student')

        # adjust field names to match your models
        self.test = Test.objects.create(
            title='Sample', subject='Math', teacher=teacher,
            start_time=timezone.now() - timedelta(hours=1),
            last_date_for_submission=timezone.localdate() + timedelta(days=1),
            duration_minutes=30, total_marks=1, is_published=True,
        )
        self.q = Question.objects.create(test=self.test, correct_option='A')  # plus your other fields

        self.client.login(username='student1', password='pass12345')

    def test_start_creates_attempt(self):
        resp = self.client.post(reverse('StartTest', args=[self.test.id]))
        attempt = TestAttempt.objects.get(student=self.student)
        self.assertRedirects(resp, reverse('TakeTest', args=[attempt.id]), fetch_redirect_response=False)

    def test_save_and_submit_scores_correctly(self):
        self.client.post(reverse('StartTest', args=[self.test.id]))
        attempt = TestAttempt.objects.get(student=self.student)

        resp = self.client.post(
            reverse('SaveAnswer', args=[attempt.id]),
            {'question_id': self.q.id, 'selected_option': 'A'},
        )
        self.assertEqual(resp.status_code, 200)

        self.client.post(reverse('SubmitTest', args=[attempt.id]))
        attempt.refresh_from_db()
        self.assertEqual(attempt.status, 'completed')
        self.assertEqual(attempt.marks_obtained, 1)

    def test_invalid_option_rejected(self):
        self.client.post(reverse('StartTest', args=[self.test.id]))
        attempt = TestAttempt.objects.get(student=self.student)
        resp = self.client.post(
            reverse('SaveAnswer', args=[attempt.id]),
            {'question_id': self.q.id, 'selected_option': 'Z'},
        )
        self.assertEqual(resp.status_code, 400)