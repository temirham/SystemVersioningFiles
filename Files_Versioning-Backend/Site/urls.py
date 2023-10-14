from django.urls import path, include
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from Site.exceptions import django_not_found_handler, django_internal_error_handler

schema_view = get_schema_view(
   openapi.Info(
      title='Files Versioning API',
      default_version='v1',
      description='Is used to see and download soft',
      # contact=openapi.Contact(email='contact@snippets.local'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('files_versioning_api/v1/', include('FilesVersioning.api_v1.urls', namespace='files-versioning-api')),
    path('profiles_api/v1/',         include('Profiles.api_v1.urls',        namespace='profiles-api')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='API-swagger'),
    path('api.yaml', schema_view.without_ui(cache_timeout=0),         name='API-yaml'),
]

handler404 = django_not_found_handler


