from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import date
from django.conf import settings
from .models import BorrowTransaction, Fine
from books.models import Book
from users.models import MemberProfile
from .serializers import BorrowTransactionSerializer, IssueBookSerializer, ReturnBookSerializer
from users.permissions import IsAdminOrLibrarian

class BorrowTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to view transactions.
    Members can view only their own. Admins/Librarians can view all.
    """
    serializer_class = BorrowTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'LIBRARIAN']:
            return BorrowTransaction.objects.all().order_by('-issue_date')
        return BorrowTransaction.objects.filter(member__user=user).order_by('-issue_date')

class IssueBookView(views.APIView):
    permission_classes = [IsAdminOrLibrarian]

    def post(self, request):
        serializer = IssueBookSerializer(data=request.data)
        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']
            member_id = serializer.validated_data['member_id']

            book = get_object_or_404(Book, id=book_id)
            member = get_object_or_404(MemberProfile, id=member_id)

            if book.quantity < 1:
                return Response({'error': 'Book not available'}, status=status.HTTP_400_BAD_REQUEST)

            active_borrows = BorrowTransaction.objects.filter(member=member, status=BorrowTransaction.Status.ISSUED).count()
            if active_borrows >= member.max_books_allowed:
                return Response({'error': 'Member reached max book limit'}, status=status.HTTP_400_BAD_REQUEST)

            transaction = BorrowTransaction.objects.create(book=book, member=member)
            book.quantity -= 1
            book.save()

            return Response(BorrowTransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReturnBookView(views.APIView):
    permission_classes = [IsAdminOrLibrarian]

    def post(self, request):
        serializer = ReturnBookSerializer(data=request.data)
        if serializer.is_valid():
            transaction_id = serializer.validated_data['transaction_id']
            transaction = get_object_or_404(BorrowTransaction, id=transaction_id)

            if transaction.status == BorrowTransaction.Status.RETURNED:
                return Response({'error': 'Book already returned'}, status=status.HTTP_400_BAD_REQUEST)

            transaction.status = BorrowTransaction.Status.RETURNED
            transaction.return_date = date.today()
            transaction.save()

            book = transaction.book
            book.quantity += 1
            book.save()

            if transaction.is_overdue:
                overdue_days = (transaction.return_date - transaction.due_date).days
                fine_amount = overdue_days * getattr(settings, 'FINE_PER_DAY', 10.0)
                Fine.objects.create(transaction=transaction, amount=fine_amount)

            return Response(BorrowTransactionSerializer(transaction).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
