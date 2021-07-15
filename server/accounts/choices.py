from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class GroupChoices(models.TextChoices):
    READERS = 'readers', _('readers')
    WRITERS = 'writers', _('writers')
