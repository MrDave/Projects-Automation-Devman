import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import EmailField

class DevmanUser(models.Model):
    telegram_id = models.PositiveBigIntegerField(verbose_name='Telegram ID')
    first_name = models.CharField(max_length=40, verbose_name='Имя', null=True)
    created_at = models.DateTimeField(verbose_name='Время регистрации', auto_now_add=True)
    email = models.EmailField(max_length=150, default="", null=True, blank=True)
    #поле is_valid - необходимо для того, чтобы "случайные" пользователи или роботы-боты - не попадали сюда,
    # нужно будет доделать логику обработки этого поля, пока попадают ВСЕ !!!
    is_valid = models.BooleanField(default=True, null=True, blank=True)
    def __str__(self):
        return f"{self.first_name} - {self.telegram_id}"

class Project(models.Model):
    topic = models.CharField("тема проекта", max_length=80)
    project_manager = models.ForeignKey(
        User,
        verbose_name="менеджер",
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects"
    )

    def __str__(self):
        return f"{self.topic} - {self.project_manager}"


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


class Pm(DevmanUser):
    info = models.TextField(verbose_name='Дополнительная информация', null=True, blank=True)
    def __str__(self):
        return f"{self.first_name}"


class Students(models.Model):
    USER_ROLE_CHOICES = (
        ("newbie", "новичок"),
        ("newbie+", "новичок+"),
        ("junior", "джун"),
    )
    name = models.ForeignKey(DevmanUser, on_delete=models.CASCADE, related_name="devman_user")
    # name = models.ForeignKey(DevmanUser, on_delete=models.CASCADE, null=False)
    type = models.CharField(max_length=40, verbose_name='Роль', choices=USER_ROLE_CHOICES, null=True, blank=True)
    start = models.ForeignKey(StudyingTime, on_delete=models.CASCADE)
    info = models.TextField(verbose_name='Дополнительная информация', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.type}"


    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'


class Team(models.Model):

    name = models.CharField(max_length=40, verbose_name='Название команды', null=True, blank=True)

    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                )

    pmanager = models.ForeignKey(Pm,
                                 on_delete=models.CASCADE,
                                )

    student = models.ForeignKey(Students,
                                on_delete=models.CASCADE,
                                verbose_name='Ученики',
                                related_name='students',
                                )

    call_time = models.ForeignKey(StudyingTime,
                                  on_delete=models.CASCADE,
                                 )

    call_day = models.DateTimeField(verbose_name='День созвона')

    def __str__(self):
        return f"{self.name} - {self.pmanager}"


    # def save(self, *args, **kwargs):
    #     if SomeModel.objects.count() < settings.MAX_SOMEMODEL_COUNT:
    #         super().save(*args, **kwargs)
    #     raise ValidationError('Слишком много записей типа SomeModel!')
