from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Book(models.Model):
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    click_count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    
class BookView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    view_date = models.DateTimeField(auto_now_add=True)
    
    
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True , blank=True)
    last_name = models.CharField(max_length=50, null=True , blank=True)
    email = models.EmailField(null=True , blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True , blank=True)
    bio = models.TextField()

