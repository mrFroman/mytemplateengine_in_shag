
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import PasswordInput, CharField, EmailInput, ModelMultipleChoiceField
from .models import Category, Events, Client


class LoginUserForm(AuthenticationForm):
    username = CharField(
        label='Почтовый адрес',
        widget=EmailInput(attrs={
                'class': 'form-control',
                'id': 'floatingInput',
                'placeholder': 'Почта'
        })
    )
    password = CharField(
        label='Пароль',
        widget=PasswordInput(attrs={
                'class': 'form-control',
                'id': 'floatingPassword',
                'placeholder': 'Пароль',

        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


# форма регистрации
class RegisterUserForm(UserCreationForm):
    email = CharField(
        label='Почта',
        widget=EmailInput(attrs={
                'class': 'form-control',
                'id': 'floatingInput',
                'placeholder': 'Почта',
        })
    )
    password1 = CharField(
        label='Пароль',
        widget=PasswordInput(attrs={
                'class': 'form-control',
                'id': 'floatingPassword'
        })
    )
    password2 = CharField(
        label='повторите пароль',
        widget=PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'повторите пароль',
                'id': 'floatingPassword'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2']


# класс ввода форм доделать ввод форм
''' ввод афиши, баннер индивид или техническая '''
class CreateUrlPoster(forms.Form):
    poster_url = forms.URLField(max_length=100, label='Url афиши', required=False)


''' основная форма для ввода и редактирования афиши '''
class PreCreateBanner(forms.Form):
    banner_url = forms.URLField(max_length=100, label='Url баннера', required=True)


class CreateBannerPoster(forms.Form):
    title_poster = forms.CharField(widget=forms.TextInput(), label='Имя рассылки')
    is_newsite = forms.BooleanField(label='Новый дизайн', required=False)
    date_poster = forms.CharField(widget=forms.TextInput(), label='Дата и номер рассылки')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 70, 'rows': 5}), label='Текст для афиши')
    labels = forms.CharField(widget=forms.TextInput(), label='UTM-метка')
    number_phone_liks = forms.CharField(widget=forms.TextInput(), label='Ссылка на номер телефона города')
    number_phone = forms.CharField(widget=forms.TextInput(), label='Номер телефона города')


class ContentForm(forms.Form):
    name_event = forms.CharField(widget=forms.TextInput(), label='Название мероприятия')
    rate = forms.CharField(widget=forms.TextInput(), label='Ценз')
    date_event = forms.CharField(widget=forms.TextInput(), label='Дата мероприятия')
    time_event = forms.CharField(widget=forms.TextInput(), label='Время мероприятия')
    venue = forms.CharField(widget=forms.TextInput(), label='Место проведения')
    price = forms.CharField(widget=forms.TextInput(), label='Цена')


''' форма для отмены или переноса мероприятия '''
class PreTransferForm(forms.Form):
    is_newsite = forms.BooleanField(label='Новый дизайн', required=False)
    banner_url = forms.URLField(max_length=100, label='Url баннера', required=True)
    title_poster = forms.CharField(widget=forms.TextInput(), label='Имя рассылки')
    date_poster = forms.CharField(widget=forms.TextInput(), label='Дата и номер рассылки')
    labels = forms.CharField(widget=forms.TextInput(), label='UTM-метка')
    number_phone_liks = forms.CharField(widget=forms.TextInput(), label='Ссылка на номер телефона города')
    number_phone = forms.CharField(widget=forms.TextInput(), label='Номер телефона города')


class TransferForm(forms.Form):
    is_cancellation = forms.BooleanField(label='Отмена концерта', required=False)
    name_event = forms.CharField(widget=forms.TextInput(), label='Название мероприятия')
    alert_date = forms.CharField(widget=forms.TextInput(), label='Предыдущая дата мероприятия')
    date_event = forms.CharField(widget=forms.TextInput(), label='Дата мероприятия')
    time_event = forms.CharField(widget=forms.TextInput(), label='Время мероприятия')
    venue = forms.CharField(widget=forms.TextInput(), label='Место проведения')
    is_valid_new_date = forms.BooleanField(label='Действительны билеты на новую дату', required=False)
    not_valid_date = forms.CharField(widget=forms.TextInput(), required=False, label='Текст для нестандартного возврата билетов')


''' форма для выбора фильтров из базы '''
class ChoiseFilterModel(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['category_event', 'buy_ticket']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category_event'] = ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                         required=False, widget=forms.CheckboxSelectMultiple,
                                                                 label='Категории')
        self.fields['buy_ticket'] = ModelMultipleChoiceField(queryset=Events.objects.all(),
                                                     required=False, widget=forms.CheckboxSelectMultiple,
                                                             label='Купленные билеты')
        self.label_suffix = ''








