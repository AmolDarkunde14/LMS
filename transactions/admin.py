from django.contrib import admin
from .models import BorrowTransaction, Fine

class BorrowTransactionAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'issue_date', 'due_date', 'return_date', 'status', 'is_overdue')
    list_filter = ('status',)

admin.site.register(BorrowTransaction, BorrowTransactionAdmin)
admin.site.register(Fine)
