from django.db import models


class Student(models.Model):
    name = models.CharField("имя студента", max_length=200)
    STUDENT_LEVELS = [
        ("newbie", "новичок"),
        ("newbie+", "новичок+"),
        ("junior", "джун"),
    ]
    level = models.CharField("уровень студента", choices=STUDENT_LEVELS, default="newbie", max_length=8)
    is_from_far_east = models.BooleanField("студент с Дальнего Востока", default=False)

    def __str__(self):
        return self.name

