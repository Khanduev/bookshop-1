from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *
from captcha.fields import CaptchaField


# class AddBookForm(forms.Form):
#     name = forms.CharField(max_length=255, label='Загловок')
#     slug = forms.SlugField(max_length=255, label='URL')
#     artist = forms.CharField(max_length=255, label='Автор')
#     plot = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Сюжет')
#     photo = forms.ImageField(label='Фото', required=False)
#     is_published = forms.BooleanField(label='Публикация', required=False, initial=True)
#     category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Категория не выбрана')


class AddBookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"

    class Meta:
        model = Book
        fields = ['name', 'slug', 'artist', 'photo', 'plot', 'is_published', 'category']
        widgets: {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'plot': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 200:
            raise ValidationError('Длина больше 200 символов')
        return name


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']
        prepopulated_fields = {'slug': ['name']}


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    content = forms.CharField(label='Содержание', widget=forms.TextInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField(label='Каптча')
