# Generated by Django 5.1.5 on 2025-02-16 13:09

import django.db.models.deletion
import pgvector.django.vector
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cover_letters", "0001_add_vector_extension"),
        ("resumes", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Job",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "is_active",
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text="Used for soft deleting records.",
                    ),
                ),
                (
                    "job_title",
                    models.CharField(
                        help_text="The title of the job position.", max_length=255
                    ),
                ),
                (
                    "job_description",
                    models.TextField(
                        help_text="The full job description and requirements."
                    ),
                ),
                (
                    "job_embedding",
                    pgvector.django.vector.VectorField(
                        dimensions=1536,
                        help_text="Vector embedding of the job title and description.",
                    ),
                ),
                (
                    "resume",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="jobs",
                        to="resumes.resume",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="jobs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "job",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CoverLetter",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "is_active",
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text="Used for soft deleting records.",
                    ),
                ),
                (
                    "generated_cover_letter",
                    models.TextField(
                        help_text="The generated cover letter text using AI."
                    ),
                ),
                (
                    "prompt",
                    models.TextField(
                        blank=True,
                        help_text="The user-provided prompt or feedback for refining the cover letter. Optional.",
                    ),
                ),
                (
                    "revision",
                    models.PositiveIntegerField(
                        default=1,
                        help_text="The revision number of the cover letter. Incremented on each generation.",
                    ),
                ),
                (
                    "is_favorite",
                    models.BooleanField(
                        default=False,
                        help_text="Whether this cover letter is marked as a favorite for future reference.",
                    ),
                ),
                (
                    "content_embedding",
                    pgvector.django.vector.VectorField(
                        dimensions=1536,
                        help_text="Vector embedding of the cover letter content.",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cover_letters",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cover_letters",
                        to="cover_letters.job",
                    ),
                ),
            ],
            options={
                "db_table": "cover_letter",
                "abstract": False,
                "constraints": [
                    models.UniqueConstraint(
                        fields=("job", "revision"), name="unique_job_revision"
                    )
                ],
            },
        ),
    ]
