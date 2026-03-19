from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def availability_status(self):
        return self.quantity > 0

    def __str__(self):
        return f"{self.title} by {self.author}"
