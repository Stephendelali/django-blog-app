from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Post, Reaction
from .utils import fetch_devto_articles
import requests

# HOME 
class home(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Latest posts
        posts = Post.objects.all().order_by('-date_posted')[:6]
        context['posts'] = posts
        context['featured_post'] = posts.first() if posts else None

        # Featured users (top 8 active users)
        context['featured_users'] = User.objects.filter(is_active=True)[:8]

        # Trending tags
        context['trending_tags'] = Post.objects.values_list('tags__name', flat=True).distinct()[:10] if hasattr(Post, 'tags') else []

        # External articles (Dev.to)
        try:
            context['external_articles'] = fetch_devto_articles(per_page=6)
        except Exception:
            context['external_articles'] = []

        return context


# POSTS
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'recent_posts'
    paginate_by = 5

    def get_queryset(self):
        username = self.kwargs.get('username')
        self.profile_user = get_object_or_404(User, username=username)
        return Post.objects.filter(author=self.profile_user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.profile_user

        context['profile_user'] = profile_user
        # Fallback for followers and following
        context['followers_count'] = getattr(getattr(profile_user, 'profile', None), 'followers', []).count() if hasattr(profile_user, 'profile') else 0
        context['following_count'] = getattr(getattr(profile_user, 'following', None), 'count', lambda: 0)()
        context['is_following'] = self.request.user.is_authenticated and getattr(getattr(profile_user, 'profile', None), 'followers', []).filter(id=self.request.user.id).exists() if hasattr(profile_user, 'profile') else False

        # Add full_url to posts for sharing
        for post in context['recent_posts']:
            post.full_url = self.request.build_absolute_uri(post.get_absolute_url())

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        # Reactions with fallbacks
        context['reactions'] = {
            'love': getattr(post, 'love_count', 0),
            'clap': getattr(post, 'clap_count', 0),
            'bookmark': getattr(getattr(post, 'reactions_count', {}), 'get', lambda key, default: default)('bookmark', 0)
        }
        context['reaction_types'] = ['love', 'clap', 'bookmark']

        return context


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


# STATIC PAGES
class about(TemplateView):
    template_name = 'blog/about.html'


# EXTERNAL CONTENT 
def tech_feed(request):
    url = 'https://dev.to/api/articles?per_page=10'
    try:
        response = requests.get(url, timeout=5)
        articles = response.json() if response.status_code == 200 else []
    except Exception:
        articles = []
    return render(request, 'blog/tech_feed.html', {'articles': articles})


# FOLLOWING 
@login_required
@require_POST
def follow_user(request, username):
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


#  REACTIONS 
@login_required
@require_POST
def toggle_reaction(request):
    post_id = request.POST.get('post_id')
    r_type = request.POST.get('reaction_type')

    post = get_object_or_404(Post, id=post_id)

    reaction, created = Reaction.objects.get_or_create(
        user=request.user,
        post=post,
        reaction_type=r_type
    )

    if not created:
        reaction.delete()
        active = False
    else:
        active = True

    count = Reaction.objects.filter(post=post, reaction_type=r_type).count()

    return JsonResponse({'active': active, 'count': count})
