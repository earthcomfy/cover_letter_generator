from __future__ import annotations

import os

from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand


class CustomAppTemplateCommand(TemplateCommand):
    def handle_template(self, template, subdir):
        """
        Loads defined custom app template.
        """
        if template is None:
            return os.path.join(settings.BASE_DIR, "cover_letter_generator/config", subdir)

        if template.startswith("file://"):
            template = template[7:]

        expanded_template = os.path.expanduser(template)
        expanded_template = os.path.normpath(expanded_template)

        if os.path.isdir(expanded_template):
            return expanded_template

        absolute_path = self.download(template) if self.is_url(template) else os.path.abspath(expanded_template)

        if os.path.exists(absolute_path):
            return self.extract(absolute_path)

        raise CommandError(f"couldn't handle {self.app_or_project} template {template}.")
