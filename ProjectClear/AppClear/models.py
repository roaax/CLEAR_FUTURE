from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.appointment_date}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}, {self.content}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User , related_name= "likes")

    def __str__(self):
        return f"{self.user}, {self.content}"

