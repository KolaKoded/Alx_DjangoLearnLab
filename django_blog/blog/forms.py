from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from taggit.forms import TagField

from blog.models import Post, Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')


# handle the form for creating a new post
class PostForm(forms.ModelForm):
    tags = TagField(required=False)
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your comment here...',
        'rows': 4
    }))

    class Meta:
        model = Comment
        fields = ['content']
        

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search')