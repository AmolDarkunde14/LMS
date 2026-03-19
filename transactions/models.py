from django.db import models
from django.conf import settings
from books.models import Book
from users.models import MemberProfile
from datetime import date, timedelta

class BorrowTransaction(models.Model):
    class Status(models.TextChoices):
        ISSUED = 'ISSUED', 'Issued'
        RETURNED = 'RETURNED', 'Returned'
        LOST = 'LOST', 'Lost'

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='transactions')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ISSUED)

    def save(self, *args, **kwargs):
        if not self.id and not self.due_date:
            self.due_date = date.today() + timedelta(days=14)
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        if self.status == self.Status.RETURNED and self.return_date:
            return self.return_date > self.due_date
        if self.due_date:
            return date.today() > self.due_date
        return False

    def __str__(self):
        return f"{self.book.title} issued to {self.member.user.username}"


class Fine(models.Model):
    transaction = models.OneToOneField(BorrowTransaction, on_delete=models.CASCADE, related_name='fine')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Fine: {self.amount} for {self.transaction.member.user.username}"
