from django.shortcuts import render, redirect
from .models import Book
from .forms import ExampleForm
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404




# list all books in the database
@permission_required('bookshelf.can_view', raise_exception=True)
def books(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

# view for viewing a book detail
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})

# View for creating a book, requires can_create permission
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list') 
    else:
        form = ExampleForm()
    return render(request, 'example_form.html', {'form': form})

# View for editing a book, requires can_edit permission
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

# View for deleting a book, requires can_delete permission
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list') 
    return render(request, 'book_confirm_delete.html', {'book': book})


