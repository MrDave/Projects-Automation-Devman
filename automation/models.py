from django.db import models
import datetime


class DevmanUser(models.Model):
    telegram_id = models.PositiveBigIntegerField(verbose_name='Telegram ID')
    first_name = models.CharField(max_length=40, verbose_name='Имя', null=True)
    email = models.EmailField(blank=True)
    # поле is_valid - необходимо для того, чтобы "случайные" пользователи или роботы-боты - не попадали сюда,
    # нужно будет доделать логику обработки этого поля, пока попадают ВСЕ !!!
    is_valid = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} - {self.telegram_id}"


class Project(models.Model):
    topic = models.CharField("тема проекта", max_length=80)

    def __str__(self):
        return self.topic


class StudyingTime(models.Model):
    TIME_CHOICES = (
        (datetime.time(10, 00), 'с 10:00 до 10:30'),
        (datetime.time(13, 00), 'с 13:00 до 13:30'),
        (datetime.time(13, 30), 'с 13:30 до 14:00'),
        (datetime.time(14, 00), 'с 14:00 до 14:30'),
        (datetime.time(14, 30), 'с 14:30 до 15:00'),
        (datetime.time(15, 00), 'с 15:00 до 15:30'),
        (datetime.time(15, 30), 'с 15:30 до 16:00'),
        (datetime.time(16, 00), 'с 16:00 до 16:30'),
        (datetime.time(16, 30), 'с 16:30 до 17:00'),
        (datetime.time(00, 00), 'Любое-укажет ПМ'),
    )
    start_time = models.TimeField(verbose_name='Время начала созвонов', choices=TIME_CHOICES)

    def __str__(self):
        return f"{self.start_time}"


class ProjectManager(DevmanUser):
    info = models.TextField(verbose_name='Дополнительная информация', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name}"


class StudyGroup(models.Model):

    name = models.CharField(max_length=40, verbose_name='Название команды', null=True, blank=True)

    project = models.ForeignKey(Project, verbose_name="проект", on_delete=models.CASCADE, related_name="groups")
    manager = models.ForeignKey(ProjectManager, verbose_name="менеджер", on_delete=models.SET_NULL, null=True)
    call_time = models.ForeignKey(StudyingTime, on_delete=models.SET_NULL)
    call_day = models.DateTimeField(verbose_name="день созвона")

    def __str__(self):
        return f"{self.name} - {self.manager}"


class Student(models.Model):
    STUDENT_LEVELS = [
        ("newbie", "новичок"),
        ("newbie_plus", "новичок+"),
        ("junior", "джун"),
    ]
    user = models.ForeignKey(DevmanUser, on_delete=models.CASCADE, related_name="devman_user")
    level = models.CharField("уровень студента", choices=STUDENT_LEVELS, default="newbie", max_length=12)
    preferred_time = models.ForeignKey(StudyingTime, on_delete=models.SET_DEFAULT, default="любое время")
    info = models.TextField(verbose_name='Дополнительная информация', null=True, blank=True)
    current_group = models.ForeignKey(
        StudyGroup,
        verbose_name="текущая группа",
        on_delete=models.SET_NULL,
        null=True,
        related_name="groups"
    )

    def __str__(self):
        return str(self.user)
