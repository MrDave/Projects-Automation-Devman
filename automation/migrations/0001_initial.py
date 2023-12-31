# Generated by Django 4.2.6 on 2023-10-27 07:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DevmanUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.PositiveBigIntegerField(verbose_name='Telegram ID')),
                ('first_name', models.CharField(max_length=40, null=True, verbose_name='Имя')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('is_valid', models.BooleanField(blank=True, default=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=80, verbose_name='тема проекта')),
            ],
        ),
        migrations.CreateModel(
            name='StudyingTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(choices=[(datetime.time(10, 0), 'с 10:00 до 10:30'), (datetime.time(13, 0), 'с 13:00 до 13:30'), (datetime.time(13, 30), 'с 13:30 до 14:00'), (datetime.time(14, 0), 'с 14:00 до 14:30'), (datetime.time(14, 30), 'с 14:30 до 15:00'), (datetime.time(15, 0), 'с 15:00 до 15:30'), (datetime.time(15, 30), 'с 15:30 до 16:00'), (datetime.time(16, 0), 'с 16:00 до 16:30'), (datetime.time(16, 30), 'с 16:30 до 17:00'), (datetime.time(0, 0), 'Любое-укажет ПМ')], verbose_name='Время начала созвонов')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectManager',
            fields=[
                ('devmanuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='automation.devmanuser')),
                ('info', models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')),
            ],
            bases=('automation.devmanuser',),
        ),
        migrations.CreateModel(
            name='StudyGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True, verbose_name='Название команды')),
                ('call_day', models.DateTimeField(verbose_name='день созвона')),
                ('call_time', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automation.studyingtime')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='automation.project', verbose_name='проект')),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automation.projectmanager', verbose_name='менеджер')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('newbie', 'новичок'), ('newbie_plus', 'новичок+'), ('junior', 'джун')], default='newbie', max_length=12, verbose_name='уровень студента')),
                ('info', models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')),
                ('current_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='automation.studygroup', verbose_name='текущая группа')),
                ('preferred_time', models.ForeignKey(default='любое время', on_delete=django.db.models.deletion.SET_DEFAULT, to='automation.studyingtime')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devman_user', to='automation.devmanuser')),
            ],
        ),
    ]
