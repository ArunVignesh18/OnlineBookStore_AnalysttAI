from .forms import BookForm, GenreForm
from .models import Book, Genre, Cart
from django.http import JsonResponse
from .serializers import BookSerializer
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.password_validation import validate_password

@user_passes_test(lambda u: u.is_anonymous, login_url='dashboard')
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Basic validation for password
        try:
            validate_password(password)
        except ValidationError as e:
            error_message = ', '.join(e.messages)
            return render(request, 'signup.html', {'error_message': error_message})

        # Check if the password and confirm password match
        if password != confirm_password:
            error_message = 'Passwords do not match'
            return render(request, 'signup.html', {'error_message': error_message})

        try:
            user = User.objects.create_user(username=username, password=password)
            Cart.objects.create(user=user)
            return redirect('login')
        except:
            error_message = 'Username / Password Already Exists'
            return render(request, 'signup.html', {'error_message': error_message})
    return render(request, 'signup.html')

def login_view(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    return render(request, 'dashboard.html', {'books': books, 'genres': genres})

@login_required
def add_genre(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            # Check if the genre already exists
            if Genre.objects.filter(name=name).exists():
                error_message = 'Genre already exists'
                genres = Genre.objects.all()
                form = GenreForm()
                return render(request, 'add_genre.html', {'form': form, 'genres': genres, 'error_message': error_message})

            form.save()
            return redirect('add_genre')
    else:
        genres = Genre.objects.all()
        form = GenreForm()

    return render(request, 'add_genre.html', {'form': form, 'genres': genres})

@login_required
def add_book(request, book_id=None):
    if not request.user.is_superuser:
        return redirect('dashboard')

    genres = Genre.objects.all()
    form_title = 'Add Book'
    submit_button_label = 'Submit'

    if book_id:
        book = get_object_or_404(Book, id=book_id)
        form_title = 'Edit Book'
        submit_button_label = 'Save Changes'
    else:
        book = None

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()

            # Clear existing genres and add the selected ones
            book.genres.clear()
            genres_selected = request.POST.getlist('genres')
            for genre_id in genres_selected:
                genre = Genre.objects.get(id=genre_id)
                book.genres.add(genre)

            return redirect('dashboard')
    else:
        form = BookForm(instance=book)

    return render(request, 'book_form.html', {'form': form, 'genres': genres, 'form_title': form_title, 'submit_button_label': submit_button_label})

@login_required
def book_detail(request, book_id):
    print("\n\n\nBOOK DETAIL\n\n\n")
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book.html', {'book': book})

@login_required
def removeBook(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.user.is_superuser:
        book.delete()
        messages.success(request, 'Book removed successfully.')
        return redirect('dashboard')
    print("\n\n\nNOT REMOVING\n\n\n")
    return render(request, 'book.html', {'book': book})

@login_required
def cart_view(request):
    books = request.user.cart.books.all()
    total_price = books.aggregate(total=Sum('price'))['total'] or 0
    return render(request, 'cart.html', {'books': books, 'total_price': total_price})

@login_required
def remove_from_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    request.user.cart.books.remove(book)
    messages.success(request, 'Book removed from cart successfully.')
    return redirect('cart')

@login_required
@api_view(['GET'])
def book_list_api(request):
    books = Book.objects.all()
    print("\n\n\nBOOK LIST API\n\n\n")
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@login_required
def add_to_cart(request, book_id):
    print("\n\n\nADD TO CART\n\n\n")
    book = get_object_or_404(Book, id=book_id)
    request.user.cart.add(book)
    return redirect('dashboard')

@login_required
def remove_genre(request, genre_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    genre = get_object_or_404(Genre, id=genre_id)

    if genre.book_set.exists():
        return JsonResponse({'error': 'Genre is associated with one or more books.'}, status=400)

    genre.delete()

    return JsonResponse({'success': 'Genre removed successfully'})
