from django.contrib import admin
from .models import Student, Project


class StudentsInline(admin.TabularInline):
    model = Student
    extra = 0


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "level",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        StudentsInline
    ]
