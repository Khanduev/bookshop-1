from django.contrib import admin

from .models import *


class BookAdmin(admin.ModelAdmin):    #меняет админку
    list_display = ['id', 'slug', 'name', 'artist', 'time_create', 'time_update', 'is_published', 'category']
    list_display_links = ['id', 'slug', 'name', 'artist', 'time_create', 'time_update', 'category']
    search_fields = ['name', 'artist']
    list_filter = ['artist', 'category']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ['name']}


class CategoryAdmin(admin.ModelAdmin):    #меняет админку
    list_display = ['id', 'slug', 'name']
    list_display_links = ['id', 'slug', 'name']
    list_filter = ['id', 'name']
    prepopulated_fields = {'slug': ['name']}


admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)

