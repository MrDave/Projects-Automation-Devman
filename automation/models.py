from django.db import models
from django.contrib.auth.models import User
import datetime


class ProjectManager(models.Model):
    name = models.CharField("имя", max_length=80)
    telegram_id = models.CharField("telegram ID", max_length=80, blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Project(models.Model):
    topic = models.CharField("тема проекта", max_length=80)

    def __str__(self):
        return self.topic


class Student(models.Model):
    name = models.CharField("имя студента", max_length=200)
    telegram_id = models.CharField("telegram ID", max_length=80, blank=True)
    email = models.EmailField(blank=True)
    STUDENT_LEVELS = [
        ("newbie", "новичок"),
        ("newbie_plus", "новичок+"),
        ("junior", "джун"),
    ]
    level = models.CharField("уровень студента", choices=STUDENT_LEVELS, default="newbie", max_length=12)

    TIME_CHOICES = [
        (datetime.time(9, 0), "9:00"),
        (datetime.time(9, 30), "9:30"),
        (datetime.time(10, 0), "10:00"),
        (datetime.time(10, 30), "10:30"),
        (datetime.time(11, 0), "11:00"),
        (datetime.time(11, 30), "11:30"),
        (datetime.time(12, 0), "12:00"),
        (datetime.time(12, 30), "12:30"),
        (datetime.time(13, 0), "13:00"),
        (datetime.time(19, 0), "19:00"),
        (datetime.time(19, 30), "19:30"),
        (datetime.time(20, 0), "20:00"),
        (datetime.time(20, 30), "20:30"),
        (datetime.time(21, 0), "21:00"),
        (datetime.time(21, 30), "21:30"),
        (datetime.time(22, 0), "22:00"),
        (datetime.time(22, 30), "22:30"),
        (datetime.time(23, 0), "23:00"),
        (datetime.time(0, 0), "любое время"),
    ]
    preferred_time = models.TimeField(
        verbose_name="предпочитаемое время созвона",
        choices=TIME_CHOICES,
        default=datetime.time(0, 0)
    )

    def __str__(self):
        return self.name


class StudyGroup(models.Model):
    project = models.ForeignKey(Project, verbose_name="проект", on_delete=models.CASCADE, related_name="groups")
    manager = models.ForeignKey(ProjectManager, verbose_name="менеджер", on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(Student, verbose_name="студенты", related_name="groups")
    start_date = models.DateField(verbose_name="дата начала")
    call_time = models.TimeField(verbose_name="время созвона", null=True)
