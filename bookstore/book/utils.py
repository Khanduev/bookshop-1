from .models import *

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить категорию', 'url_name': 'add_category'},
    {'title': 'Добавить книгу', 'url_name': 'add_book'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Корзина', 'url_name': 'basket'},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        category = Category.objects.all()

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
            user_menu.pop(1)

        context['menu'] = user_menu

        context['category'] = category
        if 'cat_selected' not in context:
            context["cat_selected"] = 0
        return context
