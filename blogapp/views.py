from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.http import require_POST
import json

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # Admin → see all posts
            posts = Post.objects.all().order_by('-created_at')
        else:
            # Normal user → see only their posts
            posts = Post.objects.filter(author=request.user).order_by('-created_at')
    else:
        # Not logged in → show all posts (optional, you can restrict if you want)
        posts = Post.objects.all().order_by('-created_at')

    return render(request, 'blogapp/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blogapp/create_post.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Creates the user
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blogapp/signup.html', {'form': form})

def post_detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'blogapp/post_detail.html', {'post': post})


@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        return HttpResponseForbidden('You are not allowed to edit this post.')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blogapp/create_post.html', {'form': form, 'is_edit': True})


@login_required
@require_POST
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        return HttpResponseForbidden('You are not allowed to delete this post.')
    post.delete()
    return JsonResponse({'success': True})


def comment_list(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.order_by('-created_at')
    data = []
    for c in comments:
        data.append({
            'id': c.id,
            'author': c.author.username,
            'text': c.text,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_author': request.user.is_authenticated and c.author == request.user
        })
    return JsonResponse({'comments': data})


@login_required
@require_POST
def comment_create(request, id):
    post = get_object_or_404(Post, id=id)
    try:
        payload = json.loads(request.body.decode('utf-8'))
        text = payload.get('text', '').strip()
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Invalid request format'}, status=400)
    
    if not text:
        return JsonResponse({'success': False, 'error': 'Comment cannot be empty'}, status=400)
    
    if len(text) > 5000:
        return JsonResponse({'success': False, 'error': 'Comment is too long (max 5000 characters)'}, status=400)
    
    try:
        comment = Comment.objects.create(post=post, author=request.user, text=text)
        data = {
            'id': comment.id,
            'author': comment.author.username,
            'text': comment.text,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_author': True
        }
        return JsonResponse({'success': True, 'comment': data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Failed to create comment'}, status=500)


@login_required
@require_POST
def comment_delete(request, id, comment_id):
    try:
        comment = get_object_or_404(Comment, id=comment_id, post_id=id)
        
        if comment.author != request.user:
            return JsonResponse({'success': False, 'error': 'You can only delete your own comments'}, status=403)
        
        comment.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Failed to delete comment'}, status=500)