from django.contrib import admin
from .models import Student, Project, StudyGroup, ProjectManager, DevmanUser, StudyingTime


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "level",
        "preferred_time",
    )


@admin.register(DevmanUser)
class DevmanUserAdmin(admin.ModelAdmin):
    list_display = (
        "telegram_id",
        "first_name",
        "email",
    )


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectManager)
class ProjectManagerAdmin(admin.ModelAdmin):
    pass


@admin.register(StudyingTime)
class StudyingTimeAdmin(admin.ModelAdmin):
    pass
