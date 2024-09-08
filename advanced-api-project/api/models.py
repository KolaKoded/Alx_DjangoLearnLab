from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import django_filters

# Author model to store details about book authors
class Author(models.Model):
    # Name of the author with a maximum length of 100 characters
    name = models.CharField(max_length=100)

    # String representation of the Author object, returning the author's name
    def __str__(self):
        return f'{self.name}'

# Book model to store details about books
class Book(models.Model):
    title = models.CharField(max_length=200) # Title of the book with a maximum length of 200 characters
    
    # DateField for the publication year of the book, storing both year and full date (e.g., 2024-09-01)
    publication_year = models.IntegerField()

    # This estabblishes a foreignKey relationship with the Author model, establishing a many-to-one relationship
    # When an author is deleted, all their associated books will also be deleted (CASCADE)
    # related_name='books' allows reverse querying from Author to access all related books
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    # String representation of the Book object, returning the book's title
    def __str__(self):
        return self.title
    
class CustomUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='viewer')


    # Override groups relationship
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Provide a unique related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    # Override user_permissions relationship
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Provide a unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    # String representation of the CustomUser object, returning the username
    def __str__(self):
        return self.username

    

class BookFilter(django_filters.FilterSet):
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'author_name']
