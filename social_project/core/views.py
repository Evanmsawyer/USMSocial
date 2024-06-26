from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikedPosts, Followers, Comment, Event, Group
import time

def login(request):
    """
        Handles user login and registration.
    """
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
    """
        Renders user profile page.
    """
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
    """
        Handles user posts and comments.
    """
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
    """
        Logs out the user and redirects to login page.
    """
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def like(request):
    """
        Handles post like/unlike functionality.
    """
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
    """
        Renders posts page with user's and following users' posts.
    """
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
    """
        Handles follow/unfollow functionality for users.
    """
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
    """
        Renders search results based on user input.
    """
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
def create_event(request):
    """
        Handles creation of events by users.
    """
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
    """
        Renders events page displaying user's created events.
    """
    user_profile = Profile.objects.get(user=request.user)
    user_events = Event.objects.filter(host=user_profile).order_by('-start_time')
    return render(request, 'events.html', {'events': user_events})

@login_required(login_url='login')
def delete_post(request, post_id):
    """
            Handles deletion of posts by users with appropriate permissions.
    """
    post = Post.objects.get(pk=post_id)

    if request.method == 'POST':
        if 'comment' in request.POST:
            comment_ids = request.POST.getlist('comment')
            Comment.objects.filter(pk__in=comment_ids).delete()
        else:
            post.delete()

    return redirect(request.META.get('HTTP_REFERER'))
    
@login_required
def delete_event(request, event_id):
    """
        Handles deletion of events by users with appropriate permissions.
    """
    event = get_object_or_404(Event, pk=event_id)
    if request.user == event.host.user:
        if request.method == 'POST':
            event.delete()
            messages.success(request, 'Event deleted successfully.')
            return redirect('events')
        else:
            messages.error(request, 'Invalid request method.')
            return redirect('events')
    else:
        messages.error(request, 'You do not have permission to delete this event.')
        return redirect('events')


def index(request):
    """
        Renders the index page.
    """
    return render(request, 'index.html')


@login_required(login_url='login')
def group_list(request):
    """
        Renders the list of groups a user is in and allows creation of new groups.
    """
    user = request.user

    if request.method == 'POST':
        # create a new group
        grp = Group.objects.create(owner=user)
        grp.group_name = request.POST.get('name', '')
        grp.description = request.POST.get('description', '')
        if request.FILES.get('image') is not None:
            grp.group_img = request.FILES.get('image')
        grp.save()
        grp.members.add(user)

        return redirect(f'group/{grp.group_name}')

    # get all groups user is in
    grps = user.groups_joined.all()
    owned = Group.objects.filter(owner=request.user)
    return render(request, 'group_list.html', {'groups': grps})


@login_required(login_url='login')
def group_view(request, group_name):
    """
        Renders the group page with details and posts related to the group.
    """
    user_profile = Profile.objects.get(user=request.user)
    grp = Group.objects.get(group_name=group_name)
    posts = Post.objects.filter(group_tags=grp)

    ### ADD PERMS TO ALL POST REQUESTS ###

    if request.method == 'POST':
        action = request.POST.get('action')
        match action:
            case 'edit':
                # edit the group
                grp = Group.objects.create()

                grp.owner = user_profile
                grp.group_name = request.POST.get('group_name', '')
                grp.description = request.POST.get('description', '')
                if request.FILES.get('image') is not None:
                    grp.group_img = request.FILES.get('image')
                grp.save()
            case 'add_member':
                # add a new member by username
                username = request.POST.get('username')
                new_member = User.objects.get(username=username)
                grp.members.add(new_member)
            case 'remove_member':
                # remove an existing member
                username = request.POST.get('username')
                old_member = User.objects.get(username=username)
                grp.members.remove(old_member)
            case 'delete':
                grp.delete()
        return redirect(request.META.get('HTTP_REFERER'))

    return render(request, 'group.html',
                  {'group': grp,
                   'members': grp.members.all(),
                   'member_count': grp.members.count(),
                   'posts': posts
                   })