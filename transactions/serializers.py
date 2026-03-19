from rest_framework import serializers
from .models import BorrowTransaction, Fine
from books.serializers import BookSerializer
from users.serializers import MemberProfileSerializer

class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = '__all__'

class BorrowTransactionSerializer(serializers.ModelSerializer):
    book_details = BookSerializer(source='book', read_only=True)
    member_details = MemberProfileSerializer(source='member', read_only=True)
    fine = FineSerializer(read_only=True)
    is_overdue = serializers.ReadOnlyField()

    class Meta:
        model = BorrowTransaction
        fields = ('id', 'book', 'member', 'issue_date', 'due_date', 'return_date', 'status', 'book_details', 'member_details', 'fine', 'is_overdue')
        read_only_fields = ('issue_date', 'return_date', 'status', 'due_date')

class IssueBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    member_id = serializers.IntegerField()

class ReturnBookSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()
