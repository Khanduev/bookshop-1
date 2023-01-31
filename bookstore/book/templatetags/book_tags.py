from django import template
from book.models import *

register = template.Library()


@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag("book/list_categories.html")
def show_category(sort=None, cat_selected=0):
    if not sort:
        category = Category.objects.all()
    else:
        category = Category.objects.order_by(sort)

    return {"category": category, "cat_selected": cat_selected}


# @register.inclusion_tag("book/list_book.html")
# def show_books(sort=None):
#     if not sort:
#         books = Book.objects.all()
#     else:
#         books = Book.objects.order_by(sort)
#
#     return {"books": books}
