from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from Soft_Site.views import *
from Soft_Site.exeptions import *


urlpatterns = [
    path('admin/', admin.site.urls),

    # next 2 order important:
    path('api-auth/',                include('rest_framework.urls',      namespace='rest_framework')),
    path('soft_downloading_api/v1/', include('Soft_Loading.api_v1.urls', namespace='soft_loading_api')),
    path('soft_downloading/',        include('Soft_Loading.urls',        namespace='soft_loading')),
    # path('accounts_api/',            include('Accounts.api_v1.urls',     namespace='accounts')),
    # path('profiles_api/',            include('Pofiles.api_v1.urls',      namespace='profiles')),
    path('profiles_api/',            include('Profiles.api_v1.urls',      namespace='profiles')),
    path('', index)
]

handler404 = Default404Error
handler500 = Default500Error