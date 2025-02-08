from __future__ import annotations


class CoverLetterGenerationError(Exception):
    """
    Base exception for cover letter generation errors.
    """


class OpenAIServiceError(CoverLetterGenerationError):
    """
    Raised when OpenAI service fails.
    """
