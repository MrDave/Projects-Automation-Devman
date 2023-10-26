from django.contrib import admin

from .models import *


class StudentsInline(admin.TabularInline):
    model = Students
    extra = 0


@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "start",
    )


@admin.register(DevmanUser)
class AllDevmanUser(admin.ModelAdmin):
    list_display = (
        "telegram_id",
        "first_name",
        "created_at",
        "email",
    )


@admin.register(Team)
class StudentTeam(admin.ModelAdmin):
    list_display = (
        "name",
        "project",
        "call_time",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('topic' , 'project_manager')

admin.site.register(Pm)
admin.site.register(StudyingTime)