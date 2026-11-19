from django import forms
from .models import Test, Question


class TestCreationForm(forms.ModelForm):

    class Meta:
        model = Test

        fields = [
            'title',
            'subject',
            'start_time',
            'duration_minutes',
            'total_marks',
            'last_date_for_submission',
        ]

        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),

            'last_date_for_submission': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['start_time'].input_formats = [
            '%Y-%m-%dT%H:%M'
        ]


class QuestionCreationForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = [
            'question_text',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_option',
        ]