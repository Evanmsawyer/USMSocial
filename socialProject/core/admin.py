from django.contrib import admin
from .models import Profile, Post, LikedPosts, Followers

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikedPosts)
admin.site.register(Followers)