from __future__ import annotations

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView

from cover_letter_generator.apps.cover_letters.exceptions import OpenAIServiceError
from cover_letter_generator.apps.cover_letters.forms import CoverLetterForm
from cover_letter_generator.apps.cover_letters.models import CoverLetter, Job
from cover_letter_generator.apps.cover_letters.services import cover_letter_service
from cover_letter_generator.apps.resumes.models import Resume

logger = logging.getLogger(__name__)


class JobListView(LoginRequiredMixin, ListView):
    """
    Lists all jobs of the user with their latest cover letter.
    """

    template_name = "cover_letters/job_list.html"
    model = Job
    context_object_name = "jobs"

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user).prefetch_related("cover_letters").order_by("-created_at")


class JobDetailView(LoginRequiredMixin, DetailView):
    """
    Displays a job and all its cover letter versions.
    """

    template_name = "cover_letters/job_detail.html"
    model = Job
    context_object_name = "job"

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user).prefetch_related("cover_letters")


class CoverLetterDetailView(LoginRequiredMixin, DetailView):
    """
    Displays a single cover letter.
    """

    template_name = "cover_letters/detail.html"
    model = CoverLetter
    context_object_name = "cover_letter"
    max_revisions = 5

    def get_queryset(self):
        return CoverLetter.objects.filter(user=self.request.user)


class ToggleFavoriteCoverLetterView(LoginRequiredMixin, View):
    """
    Toggles the favorite status of a cover letter.
    """

    def post(self, request, pk):
        cover_letter = get_object_or_404(CoverLetter, id=pk)
        cover_letter.is_favorite = not cover_letter.is_favorite
        cover_letter.save()
        return render(
            request,
            "cover_letters/partials/favorite_button.html",
            {"cover_letter": cover_letter},
        )


class GenerateCoverLetterView(LoginRequiredMixin, FormView):
    """
    Generates a cover letter for a job.
    """

    template_name = "cover_letters/generate.html"
    form_class = CoverLetterForm

    @transaction.atomic
    def form_valid(self, form, resume_id=None):
        try:
            job_title = form.cleaned_data["job_title"]
            job_description = form.cleaned_data["job_description"]

            if resume_id:
                resume = get_object_or_404(Resume, id=resume_id)
            else:
                resume = Resume.objects.filter(user=self.request.user, is_primary=True).first()

            job = Job.objects.create(
                user=self.request.user,
                resume=resume,
                job_title=job_title,
                job_description=job_description,
                job_embedding=cover_letter_service.create_job_embedding(job_title, job_description),
            )
            cover_letter_content = cover_letter_service.generate_cover_letter(resume, job)
            cover_letter = CoverLetter.objects.create(
                user=self.request.user,
                job=job,
                generated_cover_letter=cover_letter_content,
                content_embedding=cover_letter_service.create_cover_letter_embedding(cover_letter_content),
            )
            return redirect("cover_letter_detail", pk=cover_letter.pk)
        except OpenAIServiceError:
            messages.error(
                self.request,
                "AI Service Error. Please try again later.",
            )
            return self.form_invalid(form)
        except Exception as e:
            logger.error("Error generating cover letter: %s", str(e))
            messages.error(self.request, "An unexpected error occurred. Please try again later.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class RefineCoverLetterView(LoginRequiredMixin, View):
    """
    Refines a cover letter based on user feedback. Maximum 5 revisions allowed per cover letter.
    """

    MAX_REVISIONS = 5

    @transaction.atomic
    def post(self, request, pk):
        try:
            original_letter = get_object_or_404(CoverLetter, id=pk, user=request.user)

            current_revision_count = CoverLetter.objects.filter(job=original_letter.job).count()

            if current_revision_count >= self.MAX_REVISIONS:
                return render(
                    request,
                    "cover_letters/partials/cover_letter_content.html",
                    {"cover_letter": original_letter},
                )

            refinement_prompt = request.POST.get("refinement_prompt")
            if not refinement_prompt:
                return render(
                    request,
                    "cover_letters/partials/cover_letter_content.html",
                    {"cover_letter": original_letter},
                )

            new_content = cover_letter_service.refine_cover_letter(
                original_letter=original_letter, prompt=refinement_prompt
            )
            new_revision = CoverLetter.objects.create(
                user=self.request.user,
                job=original_letter.job,
                generated_cover_letter=new_content,
                prompt=refinement_prompt,
                revision=current_revision_count + 1,
                content_embedding=cover_letter_service.create_cover_letter_embedding(new_content),
            )
            return render(
                request,
                "cover_letters/partials/cover_letter_content.html",
                {"cover_letter": new_revision},
            )
        except OpenAIServiceError:
            messages.error(
                self.request,
                "AI Service Error. Please try again later.",
            )
            return render(
                request,
                "cover_letters/partials/cover_letter_content.html",
                {"cover_letter": original_letter},
            )
        except Exception as e:
            logger.error("Error refining cover letter: %s", str(e))
            messages.error(self.request, "An unexpected error occurred. Please try again later.")
            return render(
                request,
                "cover_letters/partials/cover_letter_content.html",
                {"cover_letter": original_letter},
            )
