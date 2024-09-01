book = Book.objects.get(id=book.id)
print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")
