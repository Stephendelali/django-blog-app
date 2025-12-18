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
    react_to_post,
    add_comment,
    delete_comment,
    about,
)

urlpatterns = [
    # Home page
    path('', home.as_view(), name='blog-home'), 

    # User posts
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),

    # Post detail / create / update / delete
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # External tech feed
    path('tech-feed/', tech_feed, name='tech_feed'),

    # Follow / unfollow
    path('follow/<str:username>/', follow_user, name='follow-user'),

    # Reactions (matches frontend JS: /posts/1/react/)
    path('posts/<int:post_id>/react/', react_to_post, name='react-to-post'),

    # Comments
    path('posts/<int:pk>/comments/add/', add_comment, name='add-comment'),
    path('comments/<int:pk>/delete/', delete_comment, name='delete-comment'),

    # About page
    path('about/', about.as_view(), name='blog-about'), 
]
