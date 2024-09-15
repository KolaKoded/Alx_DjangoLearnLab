from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home' ),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),


    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('update-profile', views.update_profile, name='update_profile'),

    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', views.PostCreateView.as_view(), name='post_new'),  
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),


    path('posts/<int:post_id>/comment/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('posts/<int:post_id>/comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('posts/<int:post_id>/comments/', views.CommentListView.as_view(), name='comment_list'),
    path('posts/<int:post_id>/comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

    path('search/', views.SearchPostsView.as_view(), name='search_posts'),
    path('tag/<str:tag_name>/', views.TaggedPostsView.as_view(), name='tagged_posts'),

    
];