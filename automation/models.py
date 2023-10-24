from django.db import models

# Create your models here.

class DevmanUser(models.Model):
    telegram_id = models.PositiveBigIntegerField(verbose_name='Telegram ID')
    first_name = models.CharField(max_length=40, verbose_name='Имя', null=True)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)

class StudyingTime(models.Model):
    TIME_CHOICES = (
        ('from1000to1030', 'с 10:00 до 10:30'),
        ('from1300to1330', 'с 13:00 до 13:30'),
        ('from1330to1400', 'с 13:30 до 14:00'),
        ('from1400to1430', 'с 14:00 до 14:30'),
        ('from1430to1500', 'с 14:30 до 15:00'),
        ('from1500to1530', 'с 15:00 до 15:30'),
        ('from1530to1600', 'с 15:30 до 16:00'),
        ('from1530to1600', 'с 16:00 до 16:30'),
        ('from1630to1700', 'с 16:30 до 17:00'),
    )
    status = models.CharField(max_length=40, verbose_name='Статус', choices=TIME_CHOICES)

class Pm(DevmanUser):
    is_active = models.BooleanField(verbose_name='Активность', null=True)

class Students(DevmanUser):
    USER_ROLE_CHOICES = (
        ('djune', 'Джун'),
        ('new', 'Новичок'),
        ('new_plus', 'Новичок+'),
    )
    role = models.CharField(max_length=40, verbose_name='Роль', choices=USER_ROLE_CHOICES)
    is_active = models.BooleanField(verbose_name='Активность', null=True)

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'



class Team(models.Model):
    pmanager = models.OneToOneField(
        Pm,
        on_delete=models.CASCADE,
    )

    student = models.ForeignKey(Students,
                                on_delete=models.CASCADE,
                                verbose_name='ПМ',
                                # related_name='',
                                )


    call_time = models.OneToOneField(StudyingTime,
                                on_delete=models.CASCADE,
                                )

    call_day = models.DateTimeField(verbose_name='День созвона')

    # def save(self, *args, **kwargs):
    #     if SomeModel.objects.count() < settings.MAX_SOMEMODEL_COUNT:
    #         super().save(*args, **kwargs)
    #     raise ValidationError('Слишком много записей типа SomeModel!')