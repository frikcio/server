import base64

from django.contrib.auth import login, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, UpdateView, DetailView

from .forms import RegisterForm, SettingsForm
from .models import Settings
from .tasks import send_verification_email

User = get_user_model()


def change_mailing_status(request, user_pk):
    if request.POST:
        mailing_status = request.POST.get('mailing_status')
        user_settings = get_object_or_404(Settings, user__pk=user_pk)
        user_settings.periodic_mailing = True if mailing_status == 'true' else False
        user_settings.save()
        return HttpResponse("Parameter changed", status=202)
    else:
        return HttpResponseRedirect(reverse_lazy('account'))


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        # if form valid, save user and give send_verification_email to celery
        user = form.save(commit=False)
        user.is_active = False
        with transaction.atomic():
            user.save()
            Settings.objects.create(user=user)
        absolute_url = self.request.build_absolute_uri('/')
        send_verification_email.delay(user.pk, absolute_url)
        return redirect('home')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name')
    template_name = 'accounts/account.html'
    success_url = reverse_lazy('account')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['mailing_form'] = SettingsForm(self.request.POST or None,
                                     instance=get_object_or_404(Settings, user__pk=self.request.user.pk))
        return context


ACCOUNT_VERIFICATION_TOKEN = "_verification_token"


class AccountActivateView(DetailView):
    activate_ulr_token = 'activate_user'
    token_generator = default_token_generator
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('account')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        #   check link if True - activate user and redirect on user's account page,
        #   if False - display message that link is not valid
        self.valid_link = False
        self.user = self.get_user()
        if self.user is not None:
            token = kwargs['token']
            if token == self.activate_ulr_token:
                session_token = self.request.session.get(ACCOUNT_VERIFICATION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    self.valid_link = True
                    self.user.is_active = True
                    self.user.save()
                    readers_group = Group.objects.get(name='readers')
                    readers_group.user_set.add(self.user)
                    login(self.request, self.user)
                    return HttpResponseRedirect(self.success_url)
            else:
                if self.token_generator.check_token(self.user, token):
                    self.request.session[ACCOUNT_VERIFICATION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.activate_ulr_token)
                    return HttpResponseRedirect(redirect_url)
        return self.render_to_response(self.get_context_data())

    def get_user(self):
        #   return user if user has exist and None if not
        try:
            user_pk = base64.urlsafe_b64decode(self.kwargs['uid64']).decode()
            user = User.objects.get(pk=user_pk)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, KeyError):
            user = None
        return user

    def get_context_data(self, **kwargs):
        #   if all alright - add "valid_link=True" to template, else - "valid_link=False" and "form=None"
        self.object = self.get_user()
        context = super().get_context_data(**kwargs)
        if not self.valid_link:
            context.update({
                'title': 'Fail account verification',
                'valid_link': False,
                'form': None,
            })
        return context
