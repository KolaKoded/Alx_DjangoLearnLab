from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Book, Author
from django.contrib.auth import get_user_model

class BookAPITest(APITestCase):
    
    def setUp(self):

        # Create a user and authenticate
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.user.role = 'admin'  # Assuming the role is set like this
        self.user.save()

        self.client.force_authenticate(user=self.user)
        
    
    def test_create_book(self):
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="Ajayi Oluwaseun") 
        self.book1 = Book.objects.create(title="Harry Potter", author=self.author1, publication_year=2000)
        self.book2 = Book.objects.create(title="The Hobbit", author=self.author2, publication_year=1937)
        
        create_url = reverse('create')
        # Test book creation
        book_data = {
            'title': 'The Great Gatsby',
            "author": {
                "name": "Author Name"
            },
            'publication_year': 1925
        }
        response = self.client.post(create_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, 'The Great Gatsby')
    
    def test_update_book(self):
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="Ajayi Oluwaseun") 
        self.book1 = Book.objects.create(title="Harry Potter", author=self.author1, publication_year=2000)
        self.book2 = Book.objects.create(title="The Hobbit", author=self.author2, publication_year=1937)
        
        update_url = reverse('update', args=[self.book1.id])  # Assuming 'book-detail' is the name for book detail view
        update_data = {
            'title': 'Harry Potter and the Philosopher\'s Stone',
            'author': {
                'name': 'J.K. Rowling'
            },
            'publication_year': 1997
        }
        response = self.client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter and the Philosopher\'s Stone')
        self.assertEqual(self.book1.publication_year, 1997)
    
    def test_delete_book(self):
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="Ajayi Oluwaseun") 
        self.book1 = Book.objects.create(title="Harry Potter", author=self.author1, publication_year=2000)
        self.book2 = Book.objects.create(title="The Hobbit", author=self.author2, publication_year=1937)
        

        delete_url = reverse('delete', args=[self.book2.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
    
    def test_filter_books_by_author(self):
        self.author1 = Author.objects.create(name="George Orwell")
        self.author2 = Author.objects.create(name="Aldous Huxley")

        Book.objects.create(title="1984", author= self.author1, publication_year=1949)
        Book.objects.create(title="Animal Farm", author= self.author1, publication_year=1945)
        Book.objects.create(title="Brave New World", author= self.author2, publication_year=1932)

        # Filter by 'George Orwell'
        filter_url = reverse('list')
        response = self.client.get(filter_url, {'author': 'George Orwell'})
        
        # Check the status code and filtered results
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two books should match
        self.assertEqual(response.data[0]['author']['name'], 'George Orwell')
        self.assertEqual(response.data[1]['author']['name'], 'George Orwell')


    def test_search_books(self):
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="Ajayi Oluwaseun") 
        self.book1 = Book.objects.create(title="Harry Potter", author=self.author1, publication_year=2000)
        self.book2 = Book.objects.create(title="The Hobbit", author=self.author2, publication_year=1937)

        search_url = reverse('list')
        response = self.client.get(search_url, {'search': 'Harry Potter'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter')
    
    def test_order_books_by_title(self):

        self.author1 = Author.objects.create(name="George Orwell")
        self.author2 = Author.objects.create(name="Aldous Huxley")

        Book.objects.create(title="The New Age", author= self.author1, publication_year=1949)
        Book.objects.create(title="Animal Farm", author= self.author1, publication_year=1945)
        Book.objects.create(title="Brave New World", author= self.author2, publication_year=1932)

        order_url = reverse('list')
        response = self.client.get(order_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Animal Farm')
        self.assertEqual(response.data[1]['title'], 'Brave New World')
        self.assertEqual(response.data[2]['title'], 'The New Age')
    
    def test_order_books_by_publication_year(self):
        self.author1 = Author.objects.create(name="George Orwell")
        self.author2 = Author.objects.create(name="Aldous Huxley")

        Book.objects.create(title="The New Age", author= self.author1, publication_year=1949)
        Book.objects.create(title="Animal Farm", author= self.author1, publication_year=1945)
        Book.objects.create(title="Brave New World", author= self.author2, publication_year=1932)

        order_url = reverse('list')
        response = self.client.get(order_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 1932)
        self.assertEqual(response.data[1]['publication_year'], 1945)
        self.assertEqual(response.data[2]['publication_year'], 1949)

    def test_authentication_required(self):
        # Test that authentication is required for book creation
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="Ajayi Oluwaseun") 
        self.book1 = Book.objects.create(title="Harry Potter", author=self.author1, publication_year=2000)
        self.book2 = Book.objects.create(title="The Hobbit", author=self.author2, publication_year=1937)
        
        create_url = reverse('create')

        self.client.logout()  # Log out the test user
        book_data = {
            'title': '1984',
            "author": {
                "name": "George Orwell"
            },
            'publication_year': 1949
        }
        response = self.client.post(create_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

