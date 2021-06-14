from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView
from django.contrib.auth.views import PasswordResetDoneView as ResetDone
from django.contrib.auth.views import PasswordResetConfirmView as ResetConfirm
from django.contrib.auth.views import PasswordResetCompleteView as ResetComplete
from django.contrib.auth.views import PasswordChangeDoneView as ChangeDone

from django.urls import path

from user_authentication.views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('password/reset/', PasswordResetView.as_view(template_name='authentication/password_reset.html'),
         name='password_reset'),
    path('reset/done/', ResetDone.as_view(template_name='authentication/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', ResetConfirm.as_view(template_name='authentication/reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/complete/',
         ResetComplete.as_view(template_name='authentication/reset_complete.html'),
         name='password_reset_complete'),
    path('settings/password/', PasswordChangeView.as_view(template_name='authentication/password_change.html'),
         name='password_change'),
    path('settings/password/done/', ChangeDone.as_view(template_name='authentication/password_change_done.html'),
         name='password_change_done'),
]
