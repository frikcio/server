from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from accounts.forms import RegisterForm
from boards.models import UserModel, TokenModel
from django.core.mail import send_mail


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_mail('Subject here', 'Here is the message.', 
                'frikcio67@gmail.com',
                [user.email],
                fail_silently=False,
            )
            user.email_user(subject=user, message='test')
        login(self.request, user)
        return redirect('home')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = UserModel
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
