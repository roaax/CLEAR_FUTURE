from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.appointment_date}"

# we need ( adviser id and current user id )
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}, {self.content}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="graduate")
    liked_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="like")

    def __str__(self):
        return f"{self.user}, {self.liked_user}"

