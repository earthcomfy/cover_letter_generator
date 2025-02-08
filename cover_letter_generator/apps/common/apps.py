from __future__ import annotations

from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cover_letter_generator.apps.common"
