
from django import forms
from django.contrib.auth.models import User

from .models import (
    Test,
    Question,
    Profile,
    LearnerProfile,
    InstructorProfile,
)


class ProfileForm(forms.ModelForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = Profile

        fields = [
            'date_of_birth',
            'profile_picture',
            'phone_number',
            'headline',
            'bio',
            'city',
            'country',
            'linkedin_url',
            'website_url',
        ]

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'bio': forms.Textarea(
                attrs={'rows': 4}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['email'].initial = self.user.email

    def clean_email(self):
        email = self.cleaned_data['email'].strip()

        if self.user and User.objects.filter(
            email__iexact=email
        ).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError(
                'This email address is already in use.'
            )

        return email


class LearnerProfileForm(forms.ModelForm):

    class Meta:
        model = LearnerProfile

        fields = [
            'highest_education',
            'institution',
            'field_of_study',
            'current_occupation',
            'skills',
            'interests',
            'learning_goals',
            'career_goals',
        ]

        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
            'interests': forms.Textarea(attrs={'rows': 3}),
            'learning_goals': forms.Textarea(attrs={'rows': 3}),
            'career_goals': forms.Textarea(attrs={'rows': 3}),
        }


class InstructorProfileForm(forms.ModelForm):

    class Meta:
        model = InstructorProfile

        fields = [
            'qualification',
            'organization',
            'designation',
            'years_of_experience',
            'expertise',
            'certifications',
            'professional_background',
            'teaching_experience',
        ]

        widgets = {
            'expertise': forms.Textarea(attrs={'rows': 3}),
            'certifications': forms.Textarea(attrs={'rows': 3}),
            'professional_background': forms.Textarea(attrs={'rows': 3}),
            'teaching_experience': forms.Textarea(attrs={'rows': 3}),
        }


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
