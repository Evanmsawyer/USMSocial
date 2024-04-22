from django.urls import path, include
from .views import delete_post, delete_event
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('posts/', views.posts, name='posts'),
    path('like', views.like, name='like'),
    path('posted', views.posted, name='posted'),
    path('follow/<str:pk>', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('post/<uuid:post_id>/delete/', views.delete_post, name='delete_post'),
    path('create_event/', views.create_event, name='create_event'),
    path('events/', views.events, name='events'),
    path('post/delete/<int:post_id>/', delete_post, name='delete_post'),
    path('event/delete/<int:event_id>/', delete_event, name='delete_event'),
]
