
import json
import logging
import csv
from io import BytesIO
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.shortcuts import reverse, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from .models import Mainindex, Client
from .form import LoginUserForm, RegisterUserForm, PreCreateBanner, ContentForm, TransferForm, \
    PreTransferForm, CreateBannerPoster, ChoiseFilterModel
from django.views.generic import CreateView, ListView
from .servises import created_mailing_list, unpack, unpuck_banner


logger = logging.getLogger(__name__)

''' класс входа по логину '''
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse('main:index')


class LogoutUser(LogoutView):
    next_page = reverse_lazy('main:index')


''' класс регистрации на сайте '''
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('main:login')

    def get_context_date(self, **kwargs):
        context = super().get_context_date(**kwargs)
        context['title'] = 'Регистрация'
        return context


''' класс перевода формы URL '''
class Index(ListView):
    model = Mainindex
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Шаблонизатор'
        return context


''' функции для создания индивидуальной рассылки '''
def create_banner(request):
    context = {}
    if request.method == 'POST':
        form = PreCreateBanner(request.POST)
        if form.is_valid():
            try:
                context['url'] = []
                context['url'].append({
                    'banner_url': form.cleaned_data.get('banner_url'),
                })
                with open('json_url.json', 'w', encoding='utf-8') as file:
                    json.dump(context, file, indent=4)
                return redirect('main:preresult', permanent=True)
            except:
                form.errors(None, 'Ошибка добавления афиши')
    else:
        form = PreCreateBanner()

    context = {
        'title': 'Создание баннеров',
        'form': form,
        }

    return render(request, 'main/createbanner.html', context)


def preresult_html(request):
    created_mailing_list()
    with open('json_content.json', 'r', encoding='utf8') as file:
        file = json.load(file)
        content = {}
        for url in file['content0']:
             content.update(url)

    form = PreCreateBanner(initial=content)
    form2 = CreateBannerPoster(initial=content)
    form3 = ContentForm(initial=content)
    context = {
        'title': 'Редактирование баннеров',
        'form': form,
        'form2': form2,
        'form3': form3,
        }

    if request.method == 'POST':
        form = PreCreateBanner(request.POST, initial=content)
        form2 = CreateBannerPoster(request.POST, initial=content)
        form3 = ContentForm(request.POST, initial=content)

        if form.is_valid() and form2.is_valid() and form3.is_valid():
            try:
                content = {}
                content['content'] = []
                content['content'].append({
                    'banner_date': form.cleaned_data,
                    'banner_title_content': form2.cleaned_data,
                    'banner_content': form3.cleaned_data,
                })
                with open('json_content.json', 'w', encoding='utf8') as file:
                    json.dump(content, file, indent=4)

                update_type = request.POST.get('update_type')
                if update_type == 'download':
                    is_dict = unpuck_banner(content)
                    if is_dict['is_newsite'] == True:
                        myfile = render_to_string('main/result.html', is_dict)
                        f = BytesIO(myfile.encode('utf-8'))
                        return FileResponse(f, as_attachment=True, filename=f"{is_dict['date_poster']}.html")
                    else:
                        myfile = render_to_string('main/oldresult.html', is_dict)
                        f = BytesIO(myfile.encode('utf-8'))
                        return FileResponse(f, as_attachment=True, filename=f"{is_dict['date_poster']}.html")
                return redirect('main:result')
            except:
                form.errors(None, 'Ошибка редактирования афиши')
    else:
        form = PreCreateBanner()
        form2 = CreateBannerPoster()
        form3 = ContentForm()

    return render(request, 'main/preresult.html', context)


def result_html(request):
    context = {}
    is_dict = unpuck_banner(context)
    if is_dict['is_newsite'] == True:
        return render(request, 'main/result.html', is_dict)
    else:
        return render(request, 'main/oldresult.html', is_dict)


''' создание технической рассылки '''
def create_transfer(request):
    context = {}
    if request.method == 'POST':
        form = PreCreateBanner(request.POST)
        if form.is_valid():
            try:
                context['url'] = []
                context['url'].append({
                    'banner_url': form.cleaned_data.get('banner_url'),
                })
                with open('json_url.json', 'w', encoding='utf-8') as file:
                    json.dump(context, file, indent=4)
                return redirect('main:pretransfer', permanent=True)
            except:
                form.errors(None, 'Ошибка добавления афиши')
    else:
        form = PreCreateBanner()

    context = {
        'title': 'Перенос мероприятия',
        'form': form,
        }

    return render(request, 'main/createtransfer.html', context)


def pretransfer_html(request):
    created_mailing_list()
    with open('json_content.json', 'r', encoding='utf8') as file:
        file = json.load(file)
        content = {}
        for url in file['content0']:
            content.update(url)

    form = PreTransferForm(initial=content)
    form2 = TransferForm(initial=content)
    context = {
        'title': 'Редактирование технической рассылки',
        'form': form,
        'form2': form2,
    }

    if request.method == 'POST':
        form = PreTransferForm(request.POST)
        form2 = TransferForm(request.POST)
        if form.is_valid() and form2.is_valid():
            try:
                content = {}
                content['content'] = []
                content['content'].append({
                    'transfer': form.cleaned_data,
                    'transfer_date': form2.cleaned_data
                })
                with open('json_content.json', 'w', encoding='utf8') as file:
                    json.dump(content, file, indent=4)

                update_type = request.POST.get('update_type')
                if update_type == 'download':
                    is_dict = unpack(content)
                    if is_dict['is_newsite'] == True:
                        myfile = render_to_string('main/resulttransfer.html', is_dict)
                        f = BytesIO(myfile.encode('utf-8'))
                        return FileResponse(f, as_attachment=True, filename=f"{is_dict['date_poster']}.html")
                    else:
                        myfile = render_to_string('main/oldresulttranfer.html', is_dict)
                        f = BytesIO(myfile.encode('utf-8'))
                        return FileResponse(f, as_attachment=True, filename=f"{is_dict['date_poster']}.html")
                return redirect('main:resulttranfer')
            except:
                form2.errors(None, 'Ошибка редактирования афиши')

    else:
        form = PreTransferForm()
        form2 = TransferForm()

    return render(request, 'main/pretransfer.html', context)


def result_transfer(request):
    context = {}
    is_dict = unpack(context)

    if is_dict['is_newsite'] == True:
        return render(request, 'main/resulttransfer.html', is_dict)
    else:
        return render(request, 'main/oldresulttranfer.html', is_dict)


''' класс для выбора базы '''
@login_required
def create_base(request):
    form = ChoiseFilterModel()
    ss = []
    if request.method == 'POST':
        filters = {}
        for key, value in request.POST.items():
            if key in ['buy_ticket', 'category_event']:
                filters[key] = value
                ss.append(Client.objects.filter(**filters))
                response = HttpResponse(content_type='text/csv')
                writer = csv.writer(response)
                writer.writerow(['Client', 'Email'])
                for member in ss:
                    writer.writerow(member)
                response['Content-disposition'] = "attachment; filename='Client.csv'"
                return response
    else:
        form = ChoiseFilterModel()

    context = {
        'title': 'выбор базы',
        'form': form,
    }

    return render(request, 'main/showbase.html', context)

# def view_404(request, exception=None):
#     return redirect('/')

