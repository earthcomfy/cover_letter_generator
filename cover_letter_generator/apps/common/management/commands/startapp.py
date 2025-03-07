from __future__ import annotations

import os

from django.conf import settings

from cover_letter_generator.apps.common.management.templates import (
    CustomAppTemplateCommand,
)


class Command(CustomAppTemplateCommand):
    help = (
        "Creates a Django app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide an application name."

    def handle(self, **options):
        app_name = options.pop("name")
        target = None
        base_dir = settings.BASE_DIR
        if not options.pop("directory"):
            app_dir = os.path.join(base_dir, "cover_letter_generator/apps", app_name)
            os.mkdir(app_dir)
            target = app_dir
        super().handle("app", app_name, target, **options)
