from django.contrib import admin
from .models import Student, Project, StudyGroup


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "level",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    pass
