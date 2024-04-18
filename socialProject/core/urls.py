from django.urls import path
from . import views

urlpatterns = [
    path('message/', views.message_view, name='message_view'),
    path('', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]