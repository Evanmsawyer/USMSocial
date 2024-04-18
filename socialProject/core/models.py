from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    email = models.EmailField(blank=False, default="example@example.com")
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_profile_image.png')
    major = models.CharField(max_length=64)
    year = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}: {self.message}'
