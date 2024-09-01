from .models import Book
from .serializers import BookSerializer
from rest_framework import permissions

# class BookList(ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
# # Create your views here.


# using viewsets
from rest_framework import viewsets

class BookViewSet(viewsets.ModelViewSet):

    # Restrict the view to only authenticated users
    permission_classes = [permissions.IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Explanation:
# - This `BookViewSet` class uses `permissions.IsAuthenticated` to restrict access to authenticated users.
# - Any request to this viewset must include a valid token in the Authorization header.
# - Without a valid token, the request will be denied with a 401 Unauthorized error.

