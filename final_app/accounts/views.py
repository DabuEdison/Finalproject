from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Goal

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'home.html')

@login_required
def goals_view(request):
    if request.method == 'POST':
        if 'create_goal' in request.POST:
            title = request.POST.get('title')
            description = request.POST.get('description')
            Goal.objects.create(user=request.user, title=title, description=description)
            return redirect('goals')  # Refresh page to show new goal

        elif 'update_goal' in request.POST:
            goal_id = request.POST.get('goal_id')
            title = request.POST.get('title')
            description = request.POST.get('description')
            Goal.objects.filter(id=goal_id, user=request.user).update(title=title, description=description)
            return redirect('goals')

        elif 'delete_goal' in request.POST:
            goal_id = request.POST.get('goal_id')
            Goal.objects.filter(id=goal_id, user=request.user).delete()
            return redirect('goals')

    # For GET request, load user's goals
    goals = Goal.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'goals.html', {'goals': goals})

@login_required
def posts_view(request):
    user = request.user

    if request.method == 'POST':
        # Create new post
        if 'create_post' in request.POST:
            title = request.POST.get('title')
            content = request.POST.get('content')
            if title and content:
                BlogPost.objects.create(author=user, title=title, content=content)
                return redirect('posts')

        # Update existing post
        elif 'update_post' in request.POST:
            post_id = request.POST.get('post_id')
            title = request.POST.get('title')
            content = request.POST.get('content')
            try:
                post = BlogPost.objects.get(id=post_id, author=user)
                post.title = title
                post.content = content
                post.save()
                return redirect('posts')
            except BlogPost.DoesNotExist:
                pass

        # Delete post
        elif 'delete_post' in request.POST:
            post_id = request.POST.get('post_id')
            try:
                post = BlogPost.objects.get(id=post_id, author=user)
                post.delete()
                return redirect('posts')
            except BlogPost.DoesNotExist:
                pass

    posts = BlogPost.objects.filter(author=user)
    return render(request, 'posts.html', {'posts': posts})


