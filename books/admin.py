from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'quantity', 'availability_status')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('category',)

admin.site.register(Book, BookAdmin)
