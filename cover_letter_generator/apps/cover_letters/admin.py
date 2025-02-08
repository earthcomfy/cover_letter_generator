from __future__ import annotations

from django.contrib import admin

from .models import CoverLetter, Job


class CoverLetterInline(admin.TabularInline):
    model = CoverLetter
    extra = 1


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    inlines = (CoverLetterInline,)


@admin.register(CoverLetter)
class CoverLetterAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "revision")
