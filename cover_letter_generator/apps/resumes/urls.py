from __future__ import annotations

from django.urls import path

from cover_letter_generator.apps.resumes.views import (
    ResumeUploadView,
    SetPrimaryResumeView,
)

urlpatterns = [
    path("upload/", ResumeUploadView.as_view(), name="upload_resume"),
    path(
        "<int:resume_id>/set-primary/",
        SetPrimaryResumeView.as_view(),
        name="set_primary_resume",
    ),
]
