# Generated by Django 4.2 on 2023-05-02 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_customuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='courses_registered',
        ),
    ]
