# AI Cover Letter Generator
A modern web application that helps users generate and refine personalized cover letters using AI. Built with Django and powered by OpenAI's GPT models.

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)

## Features

- Generate tailored cover letters based on your resume and job descriptions
- Context handling with similar examples
- Refine generated cover letters with natural language prompts
- Track revision history
- Upload and manage multiple resumes
- Mark cover letters as favorites to influence future generations

## Technology Stack
- Django 5.1
- OpenAI GPT API
- PostgreSQL with pgvector for embeddings
- Tailwind CSS for styling
- HTMX for dynamic interactions
- Alpine.js for client-side state

## Prerequisites
- [Docker Compose](https://docs.docker.com/compose/install/)
- [uv](https://github.com/astral-sh/uv?tab=readme-ov-file#installation)
- [OpenAI API key](https://platform.openai.com/docs/quickstart)
- [Google OAuth credentials](https://developers.google.com/identity/protocols/oauth2)

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/earthcomfy/cover_letter_generator.git
   cd cover_letter_generator
   ```

2. Install the project dependencies:
   ```bash
   uv sync --all-extras --dev
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration:
   # - OPENAI_API_KEY
   # - GOOGLE_CLIENT_ID
   # - GOOGLE_CLIENT_SECRET
   ```

5. Start PostgreSQL with pgvector:
   ```bash
   docker compose up
   # This will start PostgreSQL with pgvector extension enabled
   # Default credentials:
   # - Database: cover_letter_generator
   # - User: postgres
   # - Password: postgres
   ```

6. Run migrations:
   ```bash
   uv run manage.py migrate
   ```

7. Start the development server:
   ```bash
   uv run manage.py runserver
   ```
