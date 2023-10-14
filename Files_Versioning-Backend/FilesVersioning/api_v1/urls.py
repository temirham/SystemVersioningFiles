from django.urls import path
from .views import *


app_name = 'FilesVersioning'
urlpatterns = [
    path('files',                GetFileVersionsInfo.as_view(), name='get-versions-info'),
    path('files/add',            AddFileVersion.as_view(),      name='add-version'),
    path('files/delete/version', DeleteFileVersion.as_view(),   name='delete-version'),
    path('files/delete/file',    DeleteFile.as_view(),   name='delete-version'),
    path('files/download',       DownloadFileVersion.as_view(), name='download-version'),
]
