import json
import requests

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView,
    DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Post, Reaction, Comment
from .utils import fetch_devto_articles


# =======================
# HOME
# =======================
class home(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = (
            Post.objects
            .select_related('author')
            .order_by('-date_posted')[:6]
        )

        context.update({
            'posts': posts,
            'featured_post': posts.first(),
            'featured_users': User.objects.filter(is_active=True)[:8],
        })

        if hasattr(Post, 'tags'):
            context['trending_tags'] = (
                Post.objects.values_list('tags__name', flat=True)
                .distinct()[:10]
            )
        else:
            context['trending_tags'] = []

        try:
            context['external_articles'] = fetch_devto_articles(per_page=6)
        except Exception:
            context['external_articles'] = []

        return context


# =======================
# POSTS
# =======================
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.select_related('author')



class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'recent_posts'
    paginate_by = 5

    def get_queryset(self):
        username = self.kwargs['username']
        self.profile_user = get_object_or_404(User, username=username)

        return (
            Post.objects
            .filter(author=self.profile_user)
            .select_related('author')
            .order_by('-date_posted')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.profile_user
        profile = getattr(profile_user, 'profile', None)

        context.update({
            'profile_user': profile_user,
            'followers_count': profile.followers.count() if profile else 0,
            'following_count': profile_user.following.count(),
            'is_following': (
                self.request.user.is_authenticated and
                profile.followers.filter(id=self.request.user.id).exists()
            ) if profile else False,
        })

        for post in context['recent_posts']:
            post.full_url = self.request.build_absolute_uri(post.get_absolute_url())

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        return (
            Post.objects
            .select_related('author')
            .prefetch_related(
                'reactions',
                'comments',
                'comments__author',
                'comments__author__profile',
                'comments__replies',
                'comments__replies__author',
                'comments__replies__author__profile',
            )
        )




class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        return JsonResponse({
            'authenticated': False,
            'login_url': reverse_lazy('ajax_login'),
            'message': 'Please login to create a post.'
        }, status=401)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# =======================
# STATIC PAGES
# =======================
class about(TemplateView):
    template_name = 'blog/about.html'


# =======================
# EXTERNAL CONTENT
# =======================
def tech_feed(request):
    url = 'https://dev.to/api/articles?per_page=10'
    try:
        response = requests.get(url, timeout=5)
        articles = response.json() if response.status_code == 200 else []
    except Exception:
        articles = []
    return render(request, 'blog/tech_feed.html', {'articles': articles})


# =======================
# FOLLOWING
# =======================
@login_required
@require_POST
def follow_user(request, username):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    target_user = get_object_or_404(User, username=username)
    profile = getattr(target_user, 'profile', None)
    if not profile:
        return JsonResponse({'success': False, 'error': 'Profile not found'}, status=404)

    if profile.followers.filter(id=request.user.id).exists():
        profile.followers.remove(request.user)
        action = 'unfollowed'
    else:
        profile.followers.add(request.user)
        action = 'followed'

    return JsonResponse({
        'success': True,
        'action': action,
        'followers_count': profile.followers.count()
    })


# =======================
# REACTIONS
# =======================
@login_required
@require_POST
def react_to_post(request, post_id):
    data = json.loads(request.body)
    reaction_type = data.get("reaction")

    if reaction_type not in ['love', 'clap', 'bookmark']:
        return JsonResponse({'success': False}, status=400)

    post = get_object_or_404(Post, id=post_id)

    reaction, created = Reaction.objects.get_or_create(
        user=request.user,
        post=post,
        reaction_type=reaction_type
    )

    if not created:
        reaction.delete()
        active = False
    else:
        active = True

    return JsonResponse({
        "success": True,          # ✅ REQUIRED
        "reaction": reaction_type,
        "active": active,
        "count": post.reactions.filter(
            reaction_type=reaction_type
        ).count()
    })

# =======================
# COMMENTS
# =======================
@login_required
@require_POST
def add_comment(request, pk):
    data = json.loads(request.body)
    post = get_object_or_404(Post, pk=pk)

    content = data.get('content', '').strip()
    parent_id = data.get('parent_id')

    if not content:
        return JsonResponse({'success': False}, status=400)

    comment = Comment.objects.create(
        post=post,
        author=request.user,
        content=content,
        parent_id=parent_id
    )

    return JsonResponse({
        'success': True,
        'comment': {
            'id': comment.id,
            'content': comment.content,
            'author': comment.author.username,
            'author_image': comment.author.profile.image.url,
            'is_reply': comment.is_reply,
            'parent_id': comment.parent_id,
        },
        'comments_count': post.comments.count()
    })

@login_required
@require_POST
def delete_comment(request, pk):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    comment = get_object_or_404(Comment, pk=pk)
    
    if comment.author != request.user:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    post = comment.post
    comment.delete()

    return JsonResponse({
        'success': True,
        'comments_count': post.comments.count()
    })
