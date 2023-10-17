from django.urls import path, include
from .views import *
from urllib.parse import unquote
from rest_framework.routers import DefaultRouter

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title='Soft Loading API',
      default_version='v1',
      description='Is used to see and download soft',
      # contact=openapi.Contact(email='contact@snippets.local'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
router = DefaultRouter()
router.register('man_main_cats', ManagerMainCategoriesAPIView, basename='API-main-cats')
router.register('man_sub_cats',  ManagerSubCategoriesAPIView,  basename='API-main-cats')
router.register('man_soft',      ManagerSoftAPIView,           basename='API-main-cats')
router.register('man_files',     ManagerFilesAPIView,          basename='API-main-cats')

app_name = 'Soft_Loading'
urlpatterns = [
   # Users
   path('',                                 BaseAPIView.as_view(),       name='API-base'),
   path('categories/',                      CategoriesAPIView.as_view(), name='API-categories'),
   path('platforms/',                       PlatformsAPIView.as_view(),  name='API-platforms'),
   path('soft/',                            SoftAPIView.as_view(),       name='API-soft'),
   path(unquote('soft/<str:main_cat_id>/'), SoftAPIView.as_view(),       name='API-soft'),
   path(unquote('soft/<str:main_cat_id>/<str:sub_cat_id>/'),
                                            SoftAPIView.as_view(),       name='API-soft'),
   path('soft_data/<int:soft_id>/',         SoftAPIView.as_view(),       name='API-soft-data'),
   path('files/<int:file_id>/',             FileAPIView.as_view(),       name='API-file-download'),

   path('', include(router.urls)),
   #path('main_cats/', ManagerMainCategoriesAPIView.as_view(), name='API-main-cats'),
   #path('sub_cats/',  ManagerSubCategoriesAPIView.as_view(),  name='API-sub-cats'),
   #path('soft/',      ManagerSoftAPIView.as_view(),           name='API-sub-cats'),
   #path('files/',     ManagerFilesAPIView.as_view(),          name='API-sub-cats'),

   # Documentation:
   # path('file/<int:file_id>/', File1APIView.as_view(), name='API-file-download'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='API-swagger'),
   path('redoc/',   schema_view.with_ui('redoc',   cache_timeout=0), name='API-redoc'),
   path('api.yaml', schema_view.without_ui(cache_timeout=0),         name='API-yaml'),
   path('api.json', schema_view.without_ui(cache_timeout=0),         name='API-json')

]





