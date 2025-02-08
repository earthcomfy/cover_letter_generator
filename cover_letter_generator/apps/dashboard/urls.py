from __future__ import annotations

from django.urls import path

from cover_letter_generator.apps.dashboard.views import DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
]
