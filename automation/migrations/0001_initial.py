# Generated by Django 4.2.6 on 2023-10-24 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='имя студента')),
                ('level', models.CharField(choices=[('newbie', 'новичок'), ('newbie+', 'новичок+'), ('junior', 'джун')], default='newbie', max_length=8, verbose_name='уровень студента')),
                ('is_from_far_east', models.BooleanField(default=False, verbose_name='студент с Дальнего Востока')),
            ],
        ),
    ]