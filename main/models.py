from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    customer_ratings = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    genres = models.ManyToManyField(Genre)
    publication_date = models.DateField()

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    books = models.ManyToManyField(Book)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def add(self, book):
        self.books.add(book)