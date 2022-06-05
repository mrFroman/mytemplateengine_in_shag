from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'main'
urlpatterns = [
        path('', views.Index.as_view(), name='index'),
        path('login', views.LoginUser.as_view(), name='login'),
        path('logout', views.LogoutUser.as_view(), name='logout'),
        path('register', views.RegisterUser.as_view(), name='register'),
        path('createbanner/', views.create_banner, name='createbanner'),
        path('createbanner/preresult', views.preresult_html, name='preresult'),
        path('createbanner/result', views.result_html, name='result'),
        path('createbanner/oldresult', views.result_html, name='oldresult'),
        path('createtransfer/', views.create_transfer, name='createtransfer'),
        path('createtransfer/pretransfer', views.pretransfer_html, name='pretransfer'),
        path('createtransfer/resulttranfer', views.result_transfer, name='resulttranfer'),
        path('showbase', views.create_base, name='showbase'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

