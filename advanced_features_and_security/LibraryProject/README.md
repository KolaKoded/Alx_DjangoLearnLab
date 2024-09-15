# Django Permissions and Groups Configuration Guide

This guide explains how permissions and groups are configured and used within this Django application. 

## Overview

Django provides a robust permissions system that allows for granular control over what actions users can perform. Permissions can be assigned to individual users or groups of users, making it easier to manage roles within your application.

## 1. Configuring Permissions

Permissions are typically defined at the model level in Django. You can create custom permissions to specify what actions are allowed on different models.

### Defining Permissions in Models

Permissions are defined in the `Meta` class of the book model. Here’s how to define custom permissions:

```python
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title
    
```

## Applying Permissions to Users

To assign a permission to a user, use the user_permissions attribute of the User model:

```python
from django.contrib.auth.models import User, Permission

# Fetch the user and permission objects
user = User.objects.get(username='username')
permission = Permission.objects.get(codename='can_edit')

# Assign the permission to the user
user.user_permissions.add(permission)
user.save()
```

## Configuring Groups and Assigning permissions

```python
from django.contrib.auth.models import Group, Permission

# Create a new group
editors_group, created = Group.objects.get_or_create(name='Editors')

# Assign permissions to the group
can_edit_permission = Permission.objects.get(codename='can_edit')
editors_group.permissions.add(can_edit_permission)

can_create_permission = Permission.objects.get(codename='can_create')
editors_group.permissions.add(can_create_permission)

editors_group.save()
```

## Adding Users to a Group
Users can be added to groups, which grants them all the permissions associated with that group:
```python
from django.contrib.auth.models import User, Group

# Fetch the user and the group
user = User.objects.get(username='username')
editors_group = Group.objects.get(name='Editors')

# Add the user to the group
user.groups.add(editors_group)
user.save()
```

## Using Permissions and Groups in Views
Use the permission_required decorator to enforce permissions:

```python
from django.shortcuts import render, redirect
from .models import Book
from .forms import ExampleForm
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = ExampleForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=pk)  
    else:
        form = ExampleForm(instance=book)
    return render(request, 'example_form.html', {'form': form})

```