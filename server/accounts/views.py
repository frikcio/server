from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache

import base64

from .forms import RegisterForm
from boards.models import UserModel, TokenModel
from .tasks import send_verification_email


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'

    #	if form valid save user and send verification email to user
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        user_pk = user.pk
        absolute_url = self.request.build_absolute_uri('/')
        send_verification_email.delay(user_pk, absolute_url)
        return redirect('home')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = UserModel
    fields = ('first_name', 'last_name')
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


ACCOUNT_VERIFICATION_TOKEN = "_verification_token"


class AccountActivateView(UpdateView):
    model = UserModel
    activate_ulr_token = 'activate_user'
    token_generator = default_token_generator
    fields = ('first_name', 'last_name')
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('profile')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.valid_link = False
        self.user = self.get_object()
        if self.user is not None:
            token = kwargs['token']
            if token == self.activate_ulr_token:
                print("get into if")
                session_token = self.request.session.get(ACCOUNT_VERIFICATION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    self.valid_link = True
                    print("valid_link:", self.valid_link)
                    login(self.request, self.user)
                    return HttpResponseRedirect(self.success_url)
            else:
                print("i get into 'else'")
                if self.token_generator.check_token(self.user, token):
                    self.request.session[ACCOUNT_VERIFICATION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.activate_ulr_token)
                    print(redirect_url)
                    return HttpResponseRedirect(redirect_url)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        try:
            user_pk = base64.urlsafe_b64decode(self.kwargs['uid64']).decode()
            user = UserModel.objects.get(pk=user_pk)
            user.is_active = True
            user.save()
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        return user

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        print("valid_link:", self.valid_link)
        if self.valid_link:
            context['valid_link'] = True
        else:
            context.update({
                'title': 'fail account verification',
                'valid_link': False,
                'form': None,
            })
        return context
