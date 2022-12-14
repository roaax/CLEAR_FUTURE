# Generated by Django 4.1.3 on 2022-11-15 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cv',
            field=models.FileField(default='cv/', upload_to='cv/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('Adviser', 'Adviser'), ('Gradute', 'Gradute')], default='Gradute', max_length=64),
        ),
    ]
