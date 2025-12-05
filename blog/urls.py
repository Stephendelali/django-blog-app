from django.urls import path
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    LandingView,        
    GoogleLogin,
    )
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),  # <- use the correct home view
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path("google-login/", GoogleLogin.as_view(), name="google-login"),
    path("tech-feed/", views.tech_feed, name="tech_feed"),
    path('about/', views.about, name='blog-about')
]

