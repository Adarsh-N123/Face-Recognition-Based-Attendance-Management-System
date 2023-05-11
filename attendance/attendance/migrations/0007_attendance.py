# Generated by Django 4.2 on 2023-05-02 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_times_codestime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendancenumber', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('time', models.CharField(max_length=20)),
                ('coursecode', models.CharField(max_length=20)),
            ],
        ),
    ]