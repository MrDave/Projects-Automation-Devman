# Generated by Django 4.2.6 on 2023-10-28 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0007_alter_student_preferred_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='preferred_time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='automation.studyingtime', verbose_name='Время созвона'),
        ),
    ]
