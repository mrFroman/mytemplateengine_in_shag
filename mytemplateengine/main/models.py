
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

''' модели для создания пользователя и входа '''
class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Почтовый адрес должен быть задан')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields['is_staff'] = False
        extra_fields['is_superuser'] = False
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Почтовый адрес', max_length=50, db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()


''' модель для главной страницы '''
class Mainindex(models.Model):
    get_user_model()
    title = models.CharField('Название', max_length=50)

    class Meta:
        verbose_name = 'Главная'
        verbose_name_plural = 'Главная страница'


''' Модель для выбора клиентов по купленным событиям '''
class Events(models.Model):
    name_event = models.CharField('Название мероприятия', max_length=150)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория мероприятия')

    def __str__(self):
        return self.name_event


class Category(models.Model):
    name_category = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return self.name_category


class Client(models.Model):
    post_mail = models.EmailField('Почта', max_length=150)
    number_phone = models.CharField('Номер телефона', max_length=20)
    date_registratiom = models.DateField('Дата регистрации', auto_now=True)
    buy_ticket = models.ForeignKey('Events', verbose_name='купленные билеты', on_delete=models.PROTECT)
    category_event = models.ForeignKey('Category', verbose_name='категория купленных билетов', on_delete=models.PROTECT)

    def __str__(self):
        return self.post_mail




