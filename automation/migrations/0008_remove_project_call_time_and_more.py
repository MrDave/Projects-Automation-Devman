# Generated by Django 4.2.6 on 2023-10-25 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0007_remove_student_current_project_student_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='call_time',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_manager',
        ),
        migrations.RemoveField(
            model_name='project',
            name='start_date',
        ),
    ]