from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from cover_letter_generator.apps.resumes.models import Resume


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Renders the dashboard index template with the user's resumes.
    """

    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["resumes"] = Resume.objects.filter(user=self.request.user).order_by("-is_primary", "-created_at")
        return context
