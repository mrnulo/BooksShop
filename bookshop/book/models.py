from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    
    def __str__(self):
        return self.title
    
    
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.user.username