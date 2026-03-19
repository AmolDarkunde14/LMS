import random
from django.core.management.base import BaseCommand
from users.models import User, MemberProfile
from books.models import Book

class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Create Admins
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpass', role='ADMIN')
            self.stdout.write(self.style.SUCCESS('Admin created: admin / adminpass'))

        # Create Librarian
        if not User.objects.filter(username='librarian').exists():
            User.objects.create_user('librarian', 'lib@example.com', 'libpass', role='LIBRARIAN')
            self.stdout.write(self.style.SUCCESS('Librarian created: librarian / libpass'))

        # Create Members
        for i in range(1, 4):
            username = f'member{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username, f'{username}@example.com', 'pass123', role='MEMBER')
                MemberProfile.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Member created: {username} / pass123'))

        # Create Books
        books = [
            {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'isbn': '9780743273565', 'category': 'Fiction', 'quantity': 5},
            {'title': '1984', 'author': 'George Orwell', 'isbn': '9780451524935', 'category': 'Dystopian', 'quantity': 3},
            {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'isbn': '9780060935467', 'category': 'Fiction', 'quantity': 4},
            {'title': 'Clean Code', 'author': 'Robert C. Martin', 'isbn': '9780132350884', 'category': 'Technology', 'quantity': 2},
            {'title': 'Design Patterns', 'author': 'Erich Gamma', 'isbn': '9780201633610', 'category': 'Technology', 'quantity': 1},
        ]
        
        for b in books:
            book, created = Book.objects.get_or_create(isbn=b['isbn'], defaults=b)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Book created: {book.title}'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
