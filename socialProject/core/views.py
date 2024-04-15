from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User, auth
from .models import Profile


def login(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'login':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('profile')
            else:
                messages.info(request, 'Credentials Invalid')
        elif action == 'register':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email in use!')
                    return redirect('login')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Username in use!')
                    return redirect('login')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    user_model = User.objects.get(username=username)
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                    new_profile.save()
                    return redirect('login')
            else:
                messages.info(request, 'Password not matching!')
                return redirect('login')
    else:
        return render(request, 'login.html')


def profile(request):
    user_name = request.user.username
    profile = Profile.objects.get(user=request.user)
    profile_img = profile.profileimg
    return render(request, 'prof.html',{'user_name': user_name, 'profile_img': profile_img })


def logout_view(request):
    logout(request)
    return redirect('login')
