from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Book
        fields = ('title', 'author', 'publication_date', 'image')