# Generated by Django 5.1.5 on 2025-02-06 20:00

import cover_letter_generator.apps.resumes.models
import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Resume",
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
                    "name",
                    models.CharField(
                        help_text="Indicates the name of the resume to better track multiple resumes.",
                        max_length=255,
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        help_text="Indicates resume in PDF format. Size should not exceed 2 MB.",
                        upload_to="resumes/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["pdf"]
                            ),
                            cover_letter_generator.apps.resumes.models.validate_file_size,
                        ],
                    ),
                ),
                (
                    "extracted_content",
                    models.TextField(
                        help_text="Indicates extracted content from the resume. This is used for generating cover letters."
                    ),
                ),
                (
                    "is_primary",
                    models.BooleanField(
                        default=False,
                        help_text="Indicates if this is the primary resume.",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resumes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
