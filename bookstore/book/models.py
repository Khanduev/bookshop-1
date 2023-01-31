from django.db import models
from django.urls import reverse


class Book(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    artist = models.CharField(max_length=255, verbose_name="Автор")
    plot = models.TextField(verbose_name="сюжет")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_book', kwargs={'book_slug': self.slug})

    class Meta:                   #меняет оформление админки
        verbose_name = "книга"
        verbose_name_plural = "книги"
        ordering = ["-time_update", 'name']


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_category', kwargs={'category_slug': self.slug})

    class Meta:                   #меняет оформление админки
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['id']

