from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'publication_date', 'author', 'image', 'price']

class SearchForm(forms.Form):
    search_input = forms.CharField(max_length=100)