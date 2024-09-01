book.delete()
books = Book.objects.all()
print(books)  # This will output: <QuerySet []>
