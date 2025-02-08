from __future__ import annotations

from pypdf import PdfReader


class ResumeService:
    """
    Service class for handling resume-related operations.
    """

    def extract_resume_content(self, file_path: str) -> str:
        """
        Extracts text content from a PDF file.
        """
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())


resume_service = ResumeService()
