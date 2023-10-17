from django.urls import path
from Profiles.api_v1.views import SignupView, GetCSRFToken, CheckAuthenticated, LoginView, LogoutView, DeleteAccountView, GetUsersView

app_name = 'Profiles'
urlpatterns = [
    path('authenticated', CheckAuthenticated.as_view()),
    path('register', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('delete', DeleteAccountView.as_view()),
    path('csrf_cookie', GetCSRFToken.as_view()),
    path('get_users', GetUsersView.as_view()),
]