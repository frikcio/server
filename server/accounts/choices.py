from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class GroupChoices(models.TextChoices):
    READERS = 'readers', _('readers')
    WRITERS = 'writers', _('writers')


class Gender(models.TextChoices):
    NOT_SELECTED = 'u', _('unknown')
    MAN = 'm', _('man')
    WOMAN = 'w', _('woman')
