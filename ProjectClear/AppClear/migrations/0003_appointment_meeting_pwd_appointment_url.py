# Generated by Django 4.1.3 on 2022-11-16 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppClear', '0002_appointment_adviser_appointment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='meeting_pwd',
            field=models.TextField(default='-'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='url',
            field=models.TextField(default='Wait until the advisor approve the meeting'),
        ),
    ]
