from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from .models import Book
from .serializers import BookSerializer
from rest_framework import permissions
from .permissions import IsAdminOrEditor, IsAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import BookFilter


# This class-based view is used to list all books and doesnt require any permissions or authentication
class ListView(generics.ListAPIView):

    queryset = Book.objects.all() # Query all books
    serializer_class = BookSerializer  # Use the BookSerializer to serialize the data
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] # Use the DjangoFilterBackend for filtering
    filterset_class = BookFilter # Use the BookFilter class for filtering
    search_fields = ['title', 'author__name'] # Search fields for the SearchFilter
    ordering_fields = ['title', 'publication_year'] # Ordering fields for the OrderingFilter
    ordering = ['title'] # Default ordering by title


# This class-based view is used to retrieve a single book by its primary key (pk) and doesnt require any permissions or authentication
class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all() # Query all books
    serializer_class = BookSerializer # Use the BookSerializer to serialize the data

# This class-based view is used to create a new book and requires the user to be authenticated and have the role of 'admin' or 'editor'
class CreateView(generics.CreateAPIView):    
    # Permissions: Only authenticated users with the role of 'admin' or 'editor' can create a new book
    permission_classes = [permissions.IsAuthenticated, IsAdminOrEditor]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Overriding the creation process for additional validation
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # Validate the serializer data
        if serializer.is_valid():
            publication_year = serializer.validated_data.get('publication_year')
            
            current_year = date.today().year
            if publication_year > current_year:
                return Response({"publication_year": "The publication date cannot be in the future."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Save if validation passes
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# This class-based view is used to update an existing book by its primary key (pk) and requires the user to be authenticated and have the role of 'admin' or 'editor'
class UpdateView(generics.UpdateAPIView):   
    permission_classes = [permissions.IsAuthenticated, IsAdminOrEditor]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Overriding the update process for additional validation
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            publication_year = serializer.validated_data.get('publication_year')
            current_year = date.today().year
            if publication_year > current_year:
                return Response({"publication_year": "The publication date cannot be in the future."}, status=status.HTTP_400_BAD_REQUEST)

            # Save if validation passes
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# This class-based view is used to delete an existing book by its primary key (pk) and requires the user to be authenticated and have the role of 'admin'
class DeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

