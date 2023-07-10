from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.add_book, name='edit_book'),
    path('api/book_list/', views.book_list_api, name='book_list_api'),
    path('add_genre/', views.add_genre, name='add_genre'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('removeBook/<int:book_id>/', views.removeBook, name='removeBook'),
    path('remove_from_cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove_genre/<int:genre_id>/', views.remove_genre, name='remove_genre'),
]

urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)