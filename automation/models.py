from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    start_date = models.DateField("дата начала")
    topic = models.CharField("тема проекта", max_length=80)
    project_manager = models.ForeignKey(
        User,
        verbose_name="менеджер",
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects"
    )

    def __str__(self):
        return f"{self.topic} - {self.start_date}"


class Student(models.Model):
    name = models.CharField("имя студента", max_length=200)
    STUDENT_LEVELS = [
        ("newbie", "новичок"),
        ("newbie+", "новичок+"),
        ("junior", "джун"),
    ]
    level = models.CharField("уровень студента", choices=STUDENT_LEVELS, default="newbie", max_length=8)
    is_from_far_east = models.BooleanField("студент с Дальнего Востока", default=False)
    current_project = models.ForeignKey(
        Project,
        verbose_name="текущий проект",
        on_delete=models.SET_NULL,
        null=True,
        related_name="students"
    )

    def __str__(self):
        return self.name
