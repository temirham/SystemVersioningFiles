from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, \
    TokenBlacklistView, TokenVerifyView


# All requests are GET:
app_name = 'Profiles'
urlpatterns = [
    path('csrf',          GetCSRFToken.as_view(),        name='csrf-get'),
    path('token/get',     TokenObtainPairView.as_view(), name='token-get'),
    path('token/refresh', TokenRefreshView.as_view(),    name='token-refresh'),
    path('token/verify',  TokenVerifyView.as_view(),     name='token-verify'),
    path('token/logout',  TokenBlacklistView.as_view(),  name='user-logout'),

    path('signup',        AddUser.as_view(),            name='user-add'),
    path('delete',        DeleteUser.as_view(),         name='user-delete'),



    # path('user_info',     GetUserInfo.as_view(),         name='api-user-info'),
]
