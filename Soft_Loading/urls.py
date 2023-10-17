from django.urls import path, include
from urllib.parse import unquote
from .views import *

app_name = 'Soft_Loading'
urlpatterns = [
    path('<slug:language>/', include([
        path('',          filter, name='sl_filter'),
        path('login/',    login, name='sl_login'),
        path('register/', register, name='sl_register'),

        path(unquote('<str:main_cat>/'),                                     filter, name='sl_filter'),
        path(unquote('<str:main_cat>/<str:sub_cat>/'),                       filter, name='sl_filter'),
        path(unquote('<str:main_cat>/<str:sub_cat>/<int:soft_id>'),          soft_object, name='soft'),
    ])),
    path(unquote('download/<int:file_id>'), download,    name='download'),
    path('', lang_redi),
]

