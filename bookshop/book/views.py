from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from .models import Book, Author

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

@login_required
def remove_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('book_list')

@login_required
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form, 'book': book})

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Author.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('book_list')
        else:
            return redirect('login')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')