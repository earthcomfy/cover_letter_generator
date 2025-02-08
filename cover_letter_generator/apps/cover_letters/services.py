from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import backoff
from django.conf import settings
from openai import OpenAI, RateLimitError
from pgvector.django import CosineDistance

from cover_letter_generator.apps.cover_letters.exceptions import OpenAIServiceError
from cover_letter_generator.apps.cover_letters.models import CoverLetter, Job
from cover_letter_generator.apps.cover_letters.templates import (
    generation_prompt,
    refinement_prompt,
    system_prompt,
)

if TYPE_CHECKING:
    from cover_letter_generator.apps.resumes.models import Resume


logger = logging.getLogger(__name__)


class CoverLetterService:
    """
    Service class for handling cover letter generation.
    """

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.embedding_model = settings.OPENAI_API_EMBEDDING_MODEL
        self.generation_model = settings.OPENAI_API_GENERATION_MODEL

    @backoff.on_exception(backoff.expo, RateLimitError)
    def _create_embedding(self, text: str) -> list[float]:
        """
        Creates embeddings with retry logic.
        """
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error("Embedding creation failed: %s", str(e))
            raise OpenAIServiceError("Failed to create embedding") from e

    @backoff.on_exception(backoff.expo, RateLimitError)
    def _create_chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
    ) -> str:
        """
        Creates chat completions with retry logic.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.generation_model,
                messages=messages,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error("Chat completion failed: %s", str(e))
            raise OpenAIServiceError("Failed to generate content") from e

    def create_job_embedding(self, job_title: str, job_description: str) -> list[float]:
        """
        Creates and saves embeddings for a job.
        """
        job_text = f"{job_title}\n{job_description}"
        return self._create_embedding(job_text)

    def create_cover_letter_embedding(self, cover_letter: str) -> list[float]:
        """
        Creates and saves embeddings for a cover letter.
        """
        return self._create_embedding(cover_letter)

    def _find_similar_examples(self, job: Job, limit: int = 3) -> list[CoverLetter]:
        """
        Retrieves favorite cover letters that are semantically similar to a given job.
        """
        similar_letters = (
            CoverLetter.objects.filter(user=job.user, is_favorite=True)
            .annotate(similarity=CosineDistance("content_embedding", job.job_embedding))
            .filter(similarity__lte=0.5)
            .order_by("similarity")
        )
        return similar_letters[:limit] if similar_letters else []

    def generate_cover_letter(self, resume: Resume, job: Job) -> str:
        """
        Generates a cover letter using gpt-4o-mini.
        """
        similar_letters = self._find_similar_examples(job)

        examples_context = ""
        if similar_letters:
            examples_context = "\n\nReference these effective cover letters for tone and style:\n"
            for letter in similar_letters:
                examples_context += f"\n{letter.generated_cover_letter}\n"

        messages = [
            {
                "role": "system",
                "content": system_prompt.create_template(),
            },
            {
                "role": "user",
                "content": generation_prompt.create_template(
                    job_title=job.job_title,
                    job_description=job.job_description,
                    resume_content=resume.extracted_content,
                    similar_examples=examples_context,
                ),
            },
        ]
        return self._create_chat_completion(messages)

    def refine_cover_letter(self, original_letter: CoverLetter, prompt: str) -> str:
        """
        Refines an existing cover letter.
        """
        similar_letters = self._find_similar_examples(original_letter.job)

        examples_context = ""
        if similar_letters:
            examples_context = "\n\nReference these effective cover letters for tone and style:\n"
            for letter in similar_letters:
                if letter.id != original_letter.id:
                    examples_context += f"\n{letter.generated_cover_letter}\n"

        messages = [
            {
                "role": "system",
                "content": system_prompt.create_template(),
            },
            {
                "role": "user",
                "content": refinement_prompt.create_template(
                    current_letter=original_letter.generated_cover_letter,
                    refinement_prompt=prompt,
                    job_title=original_letter.job.job_title,
                    job_description=original_letter.job.job_description,
                    resume_content=original_letter.job.resume.extracted_content,
                    similar_examples=examples_context,
                ),
            },
        ]
        return self._create_chat_completion(messages)


cover_letter_service = CoverLetterService()
