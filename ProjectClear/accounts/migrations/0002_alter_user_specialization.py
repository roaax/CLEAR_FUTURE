# Generated by Django 4.1.3 on 2022-11-12 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='specialization',
            field=models.CharField(choices=[('Computer Sience', 'Computer Sience'), ('Information Technology', 'Information Technology'), ('CyberSecurity', 'Cybersecurity'), ('Archaeology', 'Archaeology'), ('Philosophy', 'Philosophy'), ('Chemistry', 'Chemistry'), ('Architectural Engineering', 'Architectural Engineering'), ('Business Administration', 'Business Administration'), ('Art Education', 'Art Education'), ('Economics', 'Economics'), ('Physics', 'Physics')], default='CyberSecurity', max_length=1024),
        ),
    ]
