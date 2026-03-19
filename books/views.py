from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from users.permissions import IsAdminOrLibrarian

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing books. List and retrieve are open to any authenticated user.
    Create, Update, Delete are restricted to Admin and Librarian.
    Supports filtering by category/author and searching by title/author/category.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'author', 'category']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrLibrarian]
        return [permission() for permission in permission_classes]
