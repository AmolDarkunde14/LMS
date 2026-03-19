from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    availability_status = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'isbn', 'category', 'quantity', 'availability_status')
