from django.urls import path
from django.views.decorators.cache import cache_page

from book.views import *

urlpatterns = [
    path('', cache_page(60)(BookHome.as_view()), name='home'),
    path('about/', about, name='about'),
    path("addcategory/", AddCategory.as_view(), name='add_category'),
    path("basket/", basket, name='basket'),
    path("account/", Account.as_view(), name='account'),
    path("login/", LoginUser.as_view(), name='login'),
    path("logout/", logout_user, name='logout'),
    path("register/", RegisterUser.as_view(), name='register'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('addbook/', AddBook.as_view(), name='add_book'),

    path('book/<slug:book_slug>/', ShowBook.as_view(), name='show_book'),
    path('category/<slug:category_slug>/', BookCategory.as_view(), name='show_category'),
]
