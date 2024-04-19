from urllib import request
from itertools import chain
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikedPosts, Followers
import time
from .forms import SearchForm


def login(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'login':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('profile', username)
            else:
                messages.info(request, 'Credentials Invalid')
                return redirect('login')
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
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_followers = len(Followers.objects.filter(user=pk))
    user_following = len(Followers.objects.filter(follower=pk))
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
        return redirect('profile', pk=request.user.username)
    posts = Post.objects.filter(user=user_profile).order_by("-created_at")
    return render(request, 'prof.html',
                  {
                      'user_profile': user_profile,
                      'posts': posts,
                      'user_object': user_object,
                      'user_posts': user_posts,
                      'user_followers': user_followers,
                      'user_following': user_following,
                  })


@login_required(login_url='login')
def posted(request):
    if request.method == 'POST':
        caption = request.POST.get('caption')
        image = request.FILES.get('image')

        if request.user.is_authenticated:
            post = Post(user=request.user, caption=caption)
            if image:
                post.image = image
            post.save()
        else:
            post = Post(caption=caption)
            if image:
                post.image = image
            post.save()

        return redirect(request.META.get('HTTP_REFERER'))

    posts = Post.objects.all()
    return render(request, 'profile.html', {'posts': posts})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def like(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikedPosts.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        add_like = LikedPosts.objects.create(post_id=post_id, username=username)
        add_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        time.sleep(1)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        time.sleep(1)
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def posts(request):
    posts = Post.objects.all().order_by("-created_at")
    profiles = Profile.objects.all()
    return render(request, 'posts.html', {'posts': posts, 'profiles': profiles})


@login_required(login_url='login')
def follow(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    is_following = Followers.objects.filter(follower=request.user, user=user_profile.user).exists()
    context = {'user_profile': user_profile, 'is_following': is_following}
    if request.method == 'POST':
        follower_username = request.POST.get('follower')
        user_username = request.POST.get('user')
        if is_following:
            Followers.objects.filter(follower=follower_username, user=user_username).delete()
        else:
            new_follower = Followers.objects.create(follower=follower_username, user=user_username)
            new_follower.save()

        return redirect(request.META.get('HTTP_REFERER'))

    return render(request, 'prof.html', context)


@login_required(login_url='login')
def search(request):
    user_object = request.user
    profile = Profile.objects.get(user=user_object)

    user_profile_li = []

    if request.method == 'POST':
        username = request.POST.get('username')
        users = User.objects.filter(username__icontains=username)

        for user in users:
            profile = Profile.objects.get(user=user)
            user_profile_li.append(profile)

    return render(request, 'search_tem.html', {'profile': profile, 'user_profile_li': user_profile_li})
