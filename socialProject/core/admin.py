from django.contrib import admin
from .models import Profile, Post, LikedPosts, Followers, Comment, Group, Event

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikedPosts)
admin.site.register(Followers)
admin.site.register(Comment)
admin.site.register(Group)
admin.site.register(Event)

