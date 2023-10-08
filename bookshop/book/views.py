
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.contrib import messages
from .forms import BookForm, ProfileForm, SearchForm
from .models import Book, Author, BookView, Profile
from django.contrib.auth.decorators import login_required
from django.utils import timezone


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
    return render(request, 'books/add_book.html', {'form': form})

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
        return render(request, 'books/edit_book.html', {'form': form, 'book': book})
    else:
        return redirect('book_list')

@login_required
def book_list(request):
    books = Book.objects.all()
    form = SearchForm()
    
    if 'cart' not in request.session:
        request.session['cart'] = []
    return render(request, 'books/book_list.html', {'books': books, 'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ایجاد پروفایل برای کاربر
            Profile.objects.create(user=user)
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

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
    return render(request, 'auth/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    
    return redirect('login')

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user
    
    # بررسی وجود ویو برای این کتاب و کاربر
    if BookView.objects.filter(user=user, book=book).exists():
        # ویو قبلاً انجام شده است
        return render(request, 'books/book_detail.html', {'book': book})
    
    # افزودن ویو به تاریخچه
    book_view = BookView(user=user, book=book)
    book_view.save()
    
    Book.objects.filter(id=book_id).update(click_count=F('click_count') + 1)
    
    return render(request, 'books/book_detail.html', {'book': book})

@login_required
def cart(request):
    cart = []
    cart_count = 0
    total_price = 0

    if 'cart' in request.session:
        cart_ids = request.session['cart']
        cart = Book.objects.filter(id__in=cart_ids)
        cart_count = len(cart_ids)

        for book in cart:
            total_price += book.price * book.quantity

    context = {
        'cart': cart,
        'cart_count': cart_count,
        'total_price': total_price
    }

    return render(request, 'books/cart.html', context)

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if 'cart' not in request.session:
        request.session['cart'] = []

    cart = request.session['cart']
    cart.append(book_id)
    request.session['cart'] = cart

    # بررسی وجود session برای تعداد کتاب‌ها
    if 'cart_count' not in request.session:
        request.session['cart_count'] = 0

    # به‌روزرسانی تعداد کتاب‌ها
    request.session['cart_count'] = len(cart)

    messages.success(request, 'The book was added to your cart.')
    return redirect('book_list')

@login_required
def remove_from_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if 'cart' in request.session:
        cart = request.session['cart']
        if book_id in cart:
            cart.remove(book_id)
            request.session['cart'] = cart

    # بررسی وجود session برای تعداد کتاب‌ها
    if 'cart_count' in request.session:
        cart_count = len(request.session['cart'])
        # بروزرسانی تعداد کتاب‌ها
        request.session['cart_count'] = cart_count
    else:
        request.session['cart_count'] = 0

    messages.success(request, 'The book was removed from your cart.')
    return redirect('cart')

@login_required
def remove_from_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if 'cart' in request.session:
        cart = request.session['cart']
        if book_id in cart:
            updated_cart = [item for item in cart if item != book_id]
            request.session['cart'] = updated_cart
            messages.success(request, 'The book was removed from your cart.')

            # به روزرسانی تعداد کتاب‌ها در سبد خرید
            cart_count = len(updated_cart)
            request.session['cart_count'] = cart_count

    return redirect('cart')

def profile_view(request):
    user = request.user
    
    # بررسی وجود پروفایل کاربر
    profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form})