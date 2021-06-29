from django.contrib.auth.mixins import LoginRequiredMixin
<<<<<<< HEAD
=======
from django.db import transaction
>>>>>>> 0d31079ddbbbbe2bbc65b675a1bb134bc83af775
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from accounts.forms import RegisterForm
from boards.models import UserModel, TokenModel
<<<<<<< HEAD
from .tasks import send_verification_email
=======
from .tasks import send_email
>>>>>>> 0d31079ddbbbbe2bbc65b675a1bb134bc83af775


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
<<<<<<< HEAD
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        user_pk = user.pk
        absolute_url = self.request.build_absolute_uri('/')
        send_verification_email.delay(user_pk, absolute_url)
=======
        with transaction.atomic():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user_pk = user.pk
            absolute_url = self.request.build_absolute_uri('/')
            send_email.delay(user_pk, absolute_url)
        login(self.request, user)
>>>>>>> 0d31079ddbbbbe2bbc65b675a1bb134bc83af775
        return redirect('home')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = UserModel
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class AccountActivateView(UpdateView):
    pass