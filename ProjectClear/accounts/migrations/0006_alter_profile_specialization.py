# Generated by Django 4.1.3 on 2022-11-12 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_profile_id_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='specialization',
            field=models.CharField(choices=[('Computer Sience', 'Computer Sience'), ('Information Technology', 'Information Technology'), ('CyberSecurity', 'Cybersecurity'), ('Archaeology', 'Archaeology'), ('Philosophy', 'Philosophy'), ('Chemistry', 'Chemistry'), ('Architectural Engineering', 'Architectural Engineering'), ('Business Administration', 'Business Administration'), ('Art Education', 'Art Education'), ('Economics', 'Economics'), ('Physics', 'Physics')], default='CyberSecurity', max_length=2048),
        ),
    ]
