from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomUserChangeForm, PostForm, CommentForm, SearchForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from datetime import datetime 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

def home(request):
    return render (request, 'post_list.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form}) 

@login_required
def profile(request): 
    return render(request, 'profile.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'update_profile.html', {'form': form})


# list all posts
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']


# detail view for a single post

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_detail')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = Comment.objects.filter(post=self.object)
        context['comments'] = comments
        context['form'] = CommentForm()
        return context

# create a new post using the post form

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    login_url = 'login'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author to the current user
        return super().form_valid(form)
    
# update a post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'tags']
    login_url = 'login'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
# delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

# view all comments under a post
class CommentListView(ListView):
    model = Comment
    template_name = 'comment_list.html'
    context_object_name = 'comments'
    ordering = ['-created_at']

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['pk'])
    
    

    
# create a new comment
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_id']})

    
# update a comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    
# delete a comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        pk = self.kwargs.get('pk') 
        return get_object_or_404(Comment, post_id=post_id, pk=pk)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        context['post'] = post
        return context
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_id']})
    
    def test_func(self):    
        comment = self.get_object()
        return self.request.user == comment.author
    
# search for posts
class SearchPostsView(ListView):
    template_name = 'search_results.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        form = SearchForm(self.request.GET or None)
        query = ''
        if form.is_valid():
            query = form.cleaned_data.get('query', '')
        
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET or None)
        return context
    

class TaggedPostsView(ListView):
    model = Post
    template_name = 'tagged_posts.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name=tag_name).distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag_name')
        return context