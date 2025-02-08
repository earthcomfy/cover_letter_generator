from __future__ import annotations

from django import forms

from cover_letter_generator.apps.resumes.models import Resume


class ResumeUploadForm(forms.ModelForm):
    """
    A form for uploading resumes.
    """

    class Meta:
        model = Resume
        fields = ("name", "file")

    name = forms.CharField(
        required=False,
        max_length=255,
        label="Name of Resume (Optional)",
        widget=forms.TextInput(
            attrs={
                "class": "shadow-sm focus:ring-indigo-500 focus:border-indigo-500 "
                "block w-full sm:text-sm border-gray-300 rounded-md"
            }
        ),
    )
    file = forms.FileField(
        label="Your resume",
        widget=forms.ClearableFileInput(
            attrs={
                "accept": ".pdf",
            }
        ),
    )
