from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    
    def __str__(self):
        return self.title
    
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
