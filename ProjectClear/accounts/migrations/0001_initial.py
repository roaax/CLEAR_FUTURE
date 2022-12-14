# Generated by Django 4.1.3 on 2022-11-12 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('age', models.IntegerField()),
                ('role', models.CharField(choices=[('Adviser', 'Adviser'), ('Gradute', 'Gradute')], default='Gradute', max_length=64)),
                ('specialization', models.CharField(choices=[('Computer Sience', 'Computer Sience'), ('Information Technology', 'Information Technology'), ('CyberSecurity', 'Cybersecurity'), ('Archaeology', 'Archaeology'), ('Philosophy', 'Philosophy'), ('Chemistry', 'Chemistry'), ('Architectural Engineering', 'Architectural Engineering'), ('Business Administration', 'Business Administration'), ('Art Education', 'Art Education'), ('Economics', 'Economics'), ('Physics', 'Physics'), ('Psychology', 'Psychology')], default='CyberSecurity', max_length=1024)),
                ('session_salary', models.FloatField()),
                ('description', models.TextField()),
                ('cv', models.FileField(upload_to='cv/')),
            ],
        ),
    ]
