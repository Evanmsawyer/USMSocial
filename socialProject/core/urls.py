from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('posts', views.posts, name='posts'),
    path('like', views.like, name='like'),
    path('posted', views.posted, name='posted'),
    path('follow/<str:pk>', views.follow, name='follow'),
    path('search', views.search, name='search')
]