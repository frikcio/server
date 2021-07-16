from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeDoneView
from django.urls import path

from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', UserUpdateView.as_view(), name='account'),
    path('account/<int:user_pk>/settings/', change_mailing_status, name='account_settings'),
    path('account/<int:user_pk>/avatar/', UploadAvatarView.as_view(), name='account_avatar'),
    path('password/reset/', PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='password_reset'),
    path('reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(template_name='accounts/reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/complete/',
         PasswordResetCompleteView.as_view(template_name='accounts/reset_complete.html'),
         name='password_reset_complete'),
    path('settings/password/', PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password_change'),
    path('settings/password/done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
    path('activate/<str:uid64>/<str:token>/', AccountActivateView.as_view(template_name='accounts/register.html'),
         name='activate_user'),
]
