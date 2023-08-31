from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookForm, SearchForm
from .models import Book, Author

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.image = form.cleaned_data['image']
            author = Author.objects.get(user=request.user)
            book.author = author
            book.save()
            messages.success(request, 'The book was successfully added.')
            return redirect('book_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = BookForm()
        form.fields['author'].queryset = Author.objects.filter(user=request.user)
    return render(request, 'add_book.html', {'form': form})

@login_required
def search_books(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            search_input = form.cleaned_data['search_input']
            books = Book.objects.filter(title__icontains=search_input)
            return render(request, 'search_results.html', {'books': books, 'search_input': search_input})
    return redirect('book_list')

@login_required
def remove_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.author.user == request.user:
        book.delete()
        messages.success(request, 'The book was successfully deleted.')
    return redirect('book_list')

@login_required
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.author.user == request.user:
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES, instance=book)
            if form.is_valid():
                book = form.save(commit=False)
                book.image = form.cleaned_data['image']
                book.save()
                messages.success(request, 'The book was successfully edited.')
                return redirect('book_list')
        else:
            form = BookForm(instance=book)
            form.fields['author'].queryset = Author.objects.filter(user=request.user)
        return render(request, 'edit_book.html', {'form': form, 'book': book})
    else:
        return redirect('book_list')

@login_required
def book_list(request):
    books = Book.objects.all()
    form = SearchForm()
    return render(request, 'book_list.html', {'books': books, 'form':form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Author.objects.create(user=user)
            messages.success(request, 'Registration successful. Please log in.')
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
            messages.success(request, 'Login successful.')
            return redirect('book_list')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('login')