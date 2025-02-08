from __future__ import annotations

from django import forms

FORM_CONTROL_CLASSES = {
    "class": (
        "shadow-sm focus:ring-indigo-500 focus:border-indigo-500 " "block w-full sm:text-sm border-gray-300 rounded-md"
    )
}


class CoverLetterForm(forms.Form):
    """
    A form for generating cover letters.
    """

    job_title = forms.CharField(
        max_length=255,
        label="Job Title",
        widget=forms.TextInput(attrs=FORM_CONTROL_CLASSES),
    )
    job_description = forms.CharField(
        label="Job Description",
        widget=forms.Textarea(attrs=FORM_CONTROL_CLASSES),
    )


class RefineCoverLetterForm(forms.Form):
    """
    A form for refining existing cover letters.
    """

    refinement_prompt = forms.CharField(
        widget=forms.Textarea(
            attrs={
                **FORM_CONTROL_CLASSES,
                "rows": "3",
                "placeholder": "Example: Make it more formal, emphasize my leadership skills, etc.",
            }
        ),
        label="How would you like to improve this cover letter?",
    )
