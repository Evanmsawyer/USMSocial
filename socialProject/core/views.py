from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
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
                return redirect('login')
        elif action == 'register':
            username = request.POST['username']
            email = request.POST['email']
            print(email)
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
                    user_model = User.objects.get(username=username, email=email)
                    new_profile = Profile.objects.create(user=user_model, email=email, id_user=user_model.id)
                    new_profile.save()
                    return redirect('login')
            else:
                messages.info(request, 'Password not matching!')
                return redirect('login')
    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def profile(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            major = request.POST['major']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            year = request.POST['year']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.major = major
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.year = year
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            major = request.POST['major']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            year = request.POST['year']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.major = major
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.year = year
            user_profile.save()
        return redirect('profile')
    return render(request, 'prof.html', {'user_profile': user_profile})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

