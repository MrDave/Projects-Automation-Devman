# Generated by Django 4.2.6 on 2023-10-25 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0005_remove_student_is_from_far_east'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='имя')),
                ('telegram_id', models.CharField(blank=True, max_length=80, verbose_name='telegram ID')),
                ('email', models.EmailField()),
            ],
        ),
    ]
