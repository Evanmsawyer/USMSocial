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


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images', blank=True)
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    liked = models.BooleanField(default=False)
    comments = models.ManyToManyField('Comment', related_name='post_comments', blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)

    def __str__(self):
        return self.user

    def get_comments(self):
        return Comment.objects.filter(post=self)

    def get_profile(self):
        return self.profile


class LikedPosts(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.post_id


class Followers(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_img = models.ImageField(upload_to='comment_images', blank=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user.username} - {self.text}"

    def get_profile(self):
        return Profile.objects.get(user=self.user)
