from __future__ import annotations

from django.urls import path

from cover_letter_generator.apps.cover_letters.views import (
    CoverLetterDetailView,
    GenerateCoverLetterView,
    JobDetailView,
    JobListView,
    RefineCoverLetterView,
    ToggleFavoriteCoverLetterView,
)

urlpatterns = [
    path("", JobListView.as_view(), name="job_list"),
    path("<int:pk>/", JobDetailView.as_view(), name="job_detail"),
    path(
        "cover-letters/<int:pk>/",
        CoverLetterDetailView.as_view(),
        name="cover_letter_detail",
    ),
    path(
        "cover-letters/generate/",
        GenerateCoverLetterView.as_view(),
        name="generate_cover_letter",
    ),
    path(
        "cover-letters/generate/<int:resume_id>/",
        GenerateCoverLetterView.as_view(),
        name="generate_cover_letter",
    ),
    path(
        "cover-letters/toggle-favorite/<int:pk>/",
        ToggleFavoriteCoverLetterView.as_view(),
        name="toggle_favorite_cover_letter",
    ),
    path(
        "cover-letters/refine/<int:pk>/",
        RefineCoverLetterView.as_view(),
        name="refine_cover_letter",
    ),
]
