from django.contrib import admin
from .models import Post
from taggit.managers import TaggableManager

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'published_date', 'author']
    search_fields = ['title', 'content']
    list_filter = ['published_date']
    date_hierarchy = 'published_date'
    ordering = ['published_date']
    tags = TaggableManager()