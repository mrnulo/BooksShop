from django import forms
from .models import Book, Profile

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'publication_date', 'author', 'image', 'price']

class SearchForm(forms.Form):
    search_input = forms.CharField(max_length=100)
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'avatar', 'bio']