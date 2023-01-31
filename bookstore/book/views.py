from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView

from .forms import *
from .models import *
from .utils import *


class BookHome(DataMixin, ListView):
    paginate_by = 20
    model = Book
    template_name = "book/mainpage.html"
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items())+list(c_def.items()))

    def get_queryset(self):
        return Book.objects.filter(is_published=True).select_related('category')


# def mainpage(request):
#     books = Book.objects.all()
#     context = {
#         "menu": menu,
#         'books': books,
#         'title': "Главная страница",
#         "cat_selected": 0,
#     }
#     return render(request, 'book/mainpage.html', context=context)


def about(request):
    context = {
        "menu": menu,
        'title': "О сайте"
    }
    return render(request, 'book/about.html', context=context)


# def show_book(request, book_slug):
#     books = get_object_or_404(Book, slug=book_slug)
#     context = {
#         "books": books,
#         "menu": menu,
#         'title': books.name,
#         "cat_selected": books.category.slug,
#     }
#     print(books.category)
#     return render(request, 'book/page.html', context=context)

class ShowBook(DataMixin, DetailView):
    model = Book
    template_name = "book/page.html"
    slug_url_kwarg = 'book_slug'
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['books'])
        return dict(list(context.items())+list(c_def.items()))


# def show_category(request, category_slug):
#     cat_id = Category.objects.filter(slug=category_slug)
#     books = Book.objects.filter(category_id=cat_id[0])
#
#     if len(books) == 0:
#         raise Http404()
#
#     context = {
#         "books": books,
#         "menu": menu,
#         'title': 'отображение по рубрикам',
#         "cat_selected": category_slug,
#     }
#     return render(request, 'book/mainpage.html', context=context)

class BookCategory(DataMixin, ListView):
    paginate_by = 20
    model = Book
    template_name = 'book/mainpage.html'
    context_object_name = 'books'
    allow_empty = False

    def get_queryset(self):
        return Book.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['category_slug'])
        c_def = self.get_user_context(title=str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items())+list(c_def.items()))


# def add_category(request):
#     if request.method == 'POST':
#         form = AddCategoryForm(request.POST, initial={'slug': 'name'})
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddCategoryForm()
#
#     context = {
#         "form": form,
#         "menu": menu,
#         'title': 'Добавить книгу',
#     }
#     return render(request, "book/add_category.html", context=context)

class AddCategory(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddCategoryForm
    template_name = "book/add_category.html"
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить категорию")
        return dict(list(context.items())+list(c_def.items()))

    def get_queryset(self):
        return Book.objects.filter(is_published=True)


class Basket(DataMixin, TemplateView):
    template_name = 'book/basket.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Корзина")
        return dict(list(context.items())+list(c_def.items()))

# def add_book(request):
#     if request.method == 'POST':
#         form = AddBookForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddBookForm()
#
#     context = {
#         "form": form,
#         "menu": menu,
#         'title': 'Добавить книгу',
#     }
#     return render(request, "book/add_book.html", context=context)

class AddBook(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddBookForm
    template_name = "book/add_book.html"
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить книгу")
        return dict(list(context.items())+list(c_def.items()))


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена<h1/>')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'book/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'book/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items())+list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'book/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class Account(DataMixin, TemplateView):
    template_name = 'book/account.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Личный кабинет")
        return dict(list(context.items())+list(c_def.items()))


