from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.models import User

from cover_letter_generator.apps.resumes.models import Resume


class ResumeInline(admin.TabularInline):
    model = Resume
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = (ResumeInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Resume)
