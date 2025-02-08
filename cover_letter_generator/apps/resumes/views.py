from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic.edit import FormView
from django_htmx.http import HttpResponseClientRefresh

from cover_letter_generator.apps.resumes.forms import ResumeUploadForm
from cover_letter_generator.apps.resumes.models import Resume
from cover_letter_generator.apps.resumes.services import resume_service


class ResumeUploadView(LoginRequiredMixin, FormView):
    """
    Uploads a resume, extracts the content and sets it as the primary resume if no other resumes exist.
    """

    template_name = "resumes/partials/upload_modal.html"
    form_class = ResumeUploadForm

    def form_valid(self, form):
        resume: Resume = form.save(commit=False)
        resume.user = self.request.user

        if not resume.name:
            resume.name = form.cleaned_data["file"].name.rsplit(".", 1)[0]

        resume.extracted_content = resume_service.extract_resume_content(form.cleaned_data["file"])

        if not Resume.objects.filter(user=self.request.user).exists():
            resume.is_primary = True

        resume.save()
        return HttpResponseClientRefresh()

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class SetPrimaryResumeView(LoginRequiredMixin, View):
    """
    Sets a resume as the primary resume.
    """

    def post(self, request, resume_id):
        resume = get_object_or_404(Resume, id=resume_id)
        Resume.objects.filter(user=self.request.user, is_primary=True).update(is_primary=False)
        resume.is_primary = True
        resume.save()
        return HttpResponseClientRefresh()
