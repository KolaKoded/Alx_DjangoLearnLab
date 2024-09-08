from django.urls import path
from .views import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # login user and generate token url
    path('token-auth/', obtain_auth_token, name='token_auth'),
    path('books/', ListView.as_view(), name='list'),
    path('books/<int:pk>/', DetailView.as_view(), name='detail'),
    path('books/create/', CreateView.as_view(), name='create'),
    path('books/update/<int:pk>/', UpdateView.as_view(), name='update'),
    path('books/delete/<int:pk>/', DeleteView.as_view(), name='delete'),
]