from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from .models import Post
import requests
from django.shortcuts import render
from .utils import fetch_devto_articles
from django.urls import reverse
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Post, Reaction
import json




# Create your views here.

def home(request):
    # Latest posts
    posts = Post.objects.all().order_by('-date_posted')[:6]

    # Featured post (most recent)
    featured_post = posts.first() if posts.exists() else None

    # Featured users (top 8 active users)
    featured_users = User.objects.filter(is_active=True)[:8]

    # Trending tags (optional, only if your Post model has tags)
    trending_tags = Post.objects.values_list('tags__name', flat=True).distinct()[:10] if hasattr(Post, 'tags') else []

    # Fetch Dev.to articles
    external_articles = fetch_devto_articles(per_page=6)

    context = {
        'posts': posts,
        'featured_post': featured_post,
        'featured_users': featured_users,
        'trending_tags': trending_tags,
        'external_articles': external_articles
    }

    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # your template
    context_object_name = 'recent_posts'
    paginate_by = 5

    def get_queryset(self):
        # Get the username from the URL
        username = self.kwargs.get('username')
        # Safely get the user, 404 if not found
        self.profile_user = get_object_or_404(User, username=username)
        # Return posts by this user
        return Post.objects.filter(author=self.profile_user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.profile_user

        # Followers and following counts
        context['followers_count'] = profile_user.profile.followers.count()  # call count()
        context['following_count'] = profile_user.following.count()  # depends on your model

        # Check if logged-in user follows this profile
        context['is_following'] = False
        if self.request.user.is_authenticated:
            context['is_following'] = profile_user.profile.followers.filter(
                id=self.request.user.id
            ).exists()

        # Pass profile_user to template
        context['profile_user'] = profile_user

        for post in context['recent_posts']:
            post.full_url = self.request.build_absolute_uri(post.get_absolute_url())

        return context
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        # Reaction counts
        context['reactions'] = {
            'love': post.clap_count,  # if using your model, otherwise post.reactions_count['love']
            'clap': post.clap_count,
            'bookmark': post.reactions_count.get('bookmark', 0)
        }

        # Pass the list of reaction types for the template
        context['reaction_types'] = ['love', 'clap', 'bookmark']

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        # Return a JSON response so JS can open modal
        return JsonResponse({
            "authenticated": False,
            "login_url": reverse_lazy("ajax_login"),
            "message": "Please login to create a post."
        }, status=401)

    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields =['title', 'content','image']

    def form_valid(self, form):
       form.instance.author = self.request.user
       return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class LandingView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.order_by('-date_posted')[:6]
        context['featured_post'] = Post.objects.order_by('-date_posted').first()
        context['featured_users'] = User.objects.filter(is_active=True)[:8]
        return context
    


from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter



def tech_feed(request):
    url = "https://dev.to/api/articles?per_page=10"
    response = requests.get(url)

    articles = response.json()

    return render(request, "blog/tech_feed.html", {"articles": articles})


def about(request):
    return render(request, 'blog/about.html',{'title':'About'})


@login_required
def follow_user(request, username):
    if request.method == "POST":
        target_user = get_object_or_404(User, username=username)
        profile = target_user.profile

        # Check if current user already follows
        if profile.followers.filter(id=request.user.id).exists():
            profile.followers.remove(request.user)
            action = "unfollowed"
        else:
            profile.followers.add(request.user)
            action = "followed"

        return JsonResponse({
            "success": True,
            "action": action,
            "followers_count": profile.followers.count()
        })

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


from django.http import JsonResponse
from .models import Reaction, Post
from django.contrib.auth.decorators import login_required

@login_required
def toggle_reaction(request):
    post_id = request.POST.get("post_id")
    r_type = request.POST.get("reaction_type")

    post = Post.objects.get(id=post_id)

    reaction, created = Reaction.objects.get_or_create(
        user=request.user,
        post=post,
        reaction_type=r_type
    )

    # If reaction already existed → remove it (toggle off)
    if not created:
        reaction.delete()
        active = False
    else:
        active = True

    count = Reaction.objects.filter(post=post, reaction_type=r_type).count()

    return JsonResponse({
        "active": active,
        "count": count
    })
