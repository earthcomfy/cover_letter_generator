from __future__ import annotations

from typing import ClassVar

from django.contrib.auth.models import User
from django.db import models
from pgvector.django import VectorField

from cover_letter_generator.apps.common.models import BaseModel
from cover_letter_generator.apps.resumes.models import Resume


class Job(BaseModel):
    """
    Represents a job posting that a user wants to apply for.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="jobs")
    job_title = models.CharField(
        max_length=255, help_text="The title of the job position."
    )
    job_description = models.TextField(
        help_text="The full job description and requirements."
    )
    job_embedding = VectorField(
        dimensions=1536,
        help_text="Vector embedding of the job title and description.",
    )

    class Meta(BaseModel.Meta):
        db_table = "job"

    def __str__(self):
        return f"{self.user}'s Job: {self.job_title}"


class CoverLetter(BaseModel):
    """
    Represents a cover letter generated for a specific job by a user.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cover_letters"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="cover_letters")
    generated_cover_letter = models.TextField(
        help_text="The generated cover letter text using AI."
    )
    prompt = models.TextField(
        help_text="The user-provided prompt or feedback for refining the cover letter. Optional.",
        blank=True,
    )
    revision = models.PositiveIntegerField(
        default=1,
        help_text="The revision number of the cover letter. Incremented on each generation.",
    )
    is_favorite = models.BooleanField(
        default=False,
        help_text="Whether this cover letter is marked as a favorite for future reference.",
    )
    content_embedding = VectorField(
        dimensions=1536, help_text="Vector embedding of the cover letter content."
    )

    class Meta(BaseModel.Meta):
        db_table = "cover_letter"
        constraints: ClassVar[list] = [
            models.UniqueConstraint(
                fields=["job", "revision"], name="unique_job_revision"
            )
        ]

    def __str__(self):
        return f"Revision {self.revision} Cover Letter for {self.job}."
