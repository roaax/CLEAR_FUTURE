# Generated by Django 4.1.3 on 2022-11-16 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AppClear', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='adviser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='booked_to', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.TextField(default='Pending'),
        ),
    ]