from __future__ import annotations

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from cover_letter_generator.apps.common.models import BaseModel


def validate_file_size(value):
    limit = 2 * 1024 * 1024  # 2 MB limit
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 2 MB.")


class Resume(BaseModel):
    """
    Model representing a user's resume.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes")
    name = models.CharField(
        max_length=255,
        help_text="Indicates the name of the resume to better track multiple resumes.",
    )
    file = models.FileField(
        upload_to="resumes/",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf"]),
            validate_file_size,
        ],
        help_text="Indicates resume in PDF format. Size should not exceed 2 MB.",
    )
    extracted_content = models.TextField(
        help_text="Indicates extracted content from the resume. This is used for generating cover letters.",
    )
    is_primary = models.BooleanField(default=False, help_text="Indicates if this is the primary resume.")

    def __str__(self):
        return f"{self.name} - {self.user}"
