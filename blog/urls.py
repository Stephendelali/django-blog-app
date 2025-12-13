from django.urls import path
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    follow_user,
    home,
    tech_feed,
    toggle_reaction,
    about,
)

urlpatterns = [
    path('', home.as_view(), name='blog-home'), 
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path("tech-feed/", tech_feed, name="tech_feed"),
    path('follow/<str:username>/', follow_user, name='follow-user'),
    path("reaction/toggle/", toggle_reaction, name="toggle-reaction"),
    path('about/', about.as_view(), name='blog-about'), 
]
