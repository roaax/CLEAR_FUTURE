from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adviser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booked_to")
    appointment_date = models.DateTimeField()
    # in Case adivser accepted the status will be changed to "Approved" else "Refused" , default is "Pending".
    status = models.TextField(default="Pending")
    url = models.TextField(default="Wait until the advisor approve the meeting")
    meeting_pwd = models.TextField(default="-")
    def __str__(self) -> str:
        return f"{self.appointment_date}"

# we need ( adviser id and current user id )
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adviser = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "adviser")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}, {self.content}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="graduate")
    liked_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="like")

    def __str__(self):
        return f"{self.user}, {self.liked_user}"

