from django.contrib import admin
from .models import Profile, Post, LikedPosts, Followers, Comment

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikedPosts)
admin.site.register(Followers)
admin.site.register(Comment)