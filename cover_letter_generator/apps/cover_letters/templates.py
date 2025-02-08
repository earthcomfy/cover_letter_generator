from __future__ import annotations

from abc import ABC, abstractmethod


class BasePromptTemplate(ABC):
    @abstractmethod
    def create_template(self, *args, **kwargs) -> str:
        pass


class SystemPromptTemplate(BasePromptTemplate):
    prompt: str = """
    You are a professional cover letter writer with 15+ years of experience.
    Your writing is clear, concise, and natural. You avoid clichés and generic phrases.
    You write in a confident but humble tone that resonates with hiring managers.

    # IMPORTANT RULES:
    - Output only the cover letter text
    - No additional commentary or meta text
    - No salutations like "Dear Hiring Manager"
    - No signatures or contact information
    - No generic phrases like "I am writing to apply"
    - Focus on specific achievements and metrics
    - Use natural, professional language
    """

    def create_template(self, *args, **kwargs) -> str:
        return self.prompt


class GenerationPromptTemplate(BasePromptTemplate):
    prompt: str = """
    # GOAL:
    Write a compelling cover letter that matches the candidate's experience with the job requirements.

    # CONTEXT:
    Role: {job_title}

    Job Description:
    {job_description}

    Candidate Background:
    {resume_content}

    {similar_examples}

    # GUIDELINES:
    1. Match specific skills and experiences to job requirements
    2. Use concrete achievements with metrics when possible
    3. Show genuine enthusiasm for the role and company
    4. Use active voice and specific examples
    5. Maintain professional tone without corporate jargon and too much adjectives
    6. End with confident call to action
    7. Conclude with "Kind regards,"

    # REMEMBER:
    - Output only the cover letter text
    - No meta text or commentary
    """

    def create_template(
        self,
        job_title: str,
        job_description: str,
        resume_content: str,
        similar_examples: str,
    ) -> str:
        return self.prompt.format(
            job_title=job_title,
            job_description=job_description,
            resume_content=resume_content,
            similar_examples=similar_examples,
        )


class RefinementPromptTemplate(BasePromptTemplate):
    prompt: str = """
    # GOAL:
    Revise the cover letter based on feedback while maintaining its strengths.

    # CURRENT VERSION:
    {current_letter}

    # REQUESTED CHANGES:
    {refinement_prompt}

    # CONTEXT:
    Role: {job_title}
    Job Requirements: {job_description}
    Candidate Background: {resume_content}

    {similar_examples}

    # GUIDELINES:
    1. Preserve effective elements from current version
    2. Implement requested changes naturally
    3. Back every statement with specific experience
    4. Use active voice and concrete examples
    5. Maintain professional tone without corporate jargon and too much adjectives
    6. Keep clear call to action
    7. End with "Kind regards,"

    # REMEMBER:
    - Output only the revised letter
    - No explanations or meta text
    """

    def create_template(
        self,
        current_letter: str,
        refinement_prompt: str,
        job_title: str,
        job_description: str,
        resume_content: str,
        similar_examples: str,
    ) -> str:
        return self.prompt.format(
            current_letter=current_letter,
            refinement_prompt=refinement_prompt,
            job_title=job_title,
            job_description=job_description,
            resume_content=resume_content,
            similar_examples=similar_examples,
        )


system_prompt = SystemPromptTemplate()
generation_prompt = GenerationPromptTemplate()
refinement_prompt = RefinementPromptTemplate()
