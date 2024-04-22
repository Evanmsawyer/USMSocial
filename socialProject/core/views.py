from urllib import request
from itertools import chain
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikedPosts, Followers, Comment, Event
from django.contrib.auth.decorators import permission_required
import time
from .forms import SearchForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Event
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


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
    is_following = Followers.objects.filter(follower=request.user, user=user_profile.user).exists()
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
                      'is_following': is_following
                  })


@login_required(login_url='login')
def posted(request):
    if request.method == 'POST':
        if 'comment' in request.POST:
            comment_text = request.POST.get('comment')
            post_id = request.POST.get('post_id')
            image = request.FILES.get('image')
            post = Post.objects.get(pk=post_id)

            comment = Comment(user=request.user, text=comment_text)
            if image:
                comment.comment_img = image
            comment.save()
            post.comments.add(comment)

            return redirect(request.META.get('HTTP_REFERER'))
        else:
            caption = request.POST.get('caption')
            image = request.FILES.get('image')

            if request.user.is_authenticated:
                profile = Profile.objects.get(user=request.user)
                post = Post(user=request.user, caption=caption, profile=profile)
                if image:
                    post.image = image
                post.save()

            return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def like(request):
    request.session['scroll_position'] = request.POST.get('scroll_position', 0)
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikedPosts.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        add_like = LikedPosts.objects.create(post_id=post_id, username=username)
        add_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.liked = True
        post.save()
        time.sleep(1)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.liked = False
        post.save()
        time.sleep(1)
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def posts(request):
    user = request.user
    user_following = Followers.objects.filter(follower=user.username).values_list('user', flat=True)
    user_posts = Post.objects.filter(user=user).order_by("-created_at")

    posts = []

    for username in user_following:
        feed_lists = Post.objects.filter(user=username).order_by("-created_at")
        posts.extend(feed_lists)
    posts.extend(user_posts)

    posts.sort(key=lambda x: x.created_at, reverse=True)

    return render(request, 'posts.html', {'posts': posts})


@login_required(login_url='login')
def follow(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    is_following = Followers.objects.filter(follower=request.user, user=user_profile.user).exists()

    if request.method == 'POST':
        follower_username = request.POST.get('follower')
        user_username = request.POST.get('user')
        if is_following:
            Followers.objects.filter(follower=follower_username, user=user_username).delete()
        else:
            new_follower = Followers.objects.create(follower=follower_username, user=user_username)
            new_follower.save()

        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def search(request):
    user_object = request.user
    profile = Profile.objects.get(user=user_object)
    user_profile_li = []

    if request.method == 'POST':
        username = request.POST.get('username')
        users = User.objects.filter(username__icontains=username)

        for user in users:
            user_profile = Profile.objects.get(user=user)
            is_following = Followers.objects.filter(follower=request.user, user=user).exists()
            user_profile_li.append({'profile': user_profile, 'is_following': is_following})

    return render(request, 'search_tem.html', {
        'profile': profile,
        'user_profile_li': user_profile_li,
    })


@login_required(login_url='login')
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)

    if request.method == 'POST':
        if 'comment' in request.POST:
            comment_ids = request.POST.getlist('comment')
            Comment.objects.filter(pk__in=comment_ids).delete()
        else:
            post.delete()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location')
        image = request.FILES.get('image')
        host_profile = Profile.objects.get(user=request.user)

        event = Event(
            host=host_profile,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            image=image
        )
        event.save()
        messages.success(request, 'Event created successfully!')
        return redirect('events')
    else:
        return render(request, 'create_event.html')

@login_required(login_url='login')
def events(request):
    user_profile = Profile.objects.get(user=request.user)
    user_events = Event.objects.filter(host=user_profile).order_by('-start_time')
    return render(request, 'events.html', {'events': user_events})

@login_required
@permission_required('your_app_name.can_delete_posts', raise_exception=True)
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.user or request.user.has_perm('your_app_name.can_delete_posts'):
        if request.method == 'POST':
            post.delete()
            messages.success(request, 'Post deleted successfully.')
            return redirect('posts')  # Redirect to the posts listing page
        else:
            messages.error(request, 'Invalid request method.')
            return redirect('posts')
    else:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('posts')
    
@login_required
@permission_required('your_app_name.can_delete_events', raise_exception=True)
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.user == event.host.user or request.user.has_perm('your_app_name.can_delete_events'):
        if request.method == 'POST':
            event.delete()
            messages.success(request, 'Event deleted successfully.')
            return redirect('events')  # Redirect to the events listing page
        else:
            messages.error(request, 'Invalid request method.')
            return redirect('events')
    else:
        messages.error(request, 'You do not have permission to delete this event.')
        return redirect('events')