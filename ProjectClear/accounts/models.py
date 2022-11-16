from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,  primary_key=True)
    image = models.ImageField(upload_to="image/")
    age = models.IntegerField()
    
    user_type_choices = models.TextChoices(" Role ", ["Adviser", "Gradute"])
    specialization_choices = models.TextChoices("Specialization List", ["Computer Sience" , "Information Technology", "CyberSecurity" , "Archaeology" ,"Philosophy" , "Chemistry" , "Architectural Engineering" , "Business Administration"
    ,"Art Education" , "Economics" , "Physics"   ])
    role  = models.CharField(max_length=64, choices = user_type_choices.choices, default=user_type_choices.Gradute)
    specialization = models.CharField(max_length=2048, choices = specialization_choices.choices, default=specialization_choices.CyberSecurity)

    session_salary = models.FloatField(default=0.0)
    description = models.TextField()
    cv = models.FileField(upload_to="cv/", default='cv/')

    def __str__(self) -> str:
        return f"{self.role}, {self.age}"

