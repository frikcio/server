
import random

from xml.sax.saxutils import escape as xml_escape

from cairosvg import svg2png
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import INITIALS_SVG_TEMPLATE


def generate_avatar(sender, instance, created, **kwargs):
    if not instance.avatar and instance.first_name and instance.last_name:
        initials = f"{instance.first_name[0]}{instance.last_name[0]}"
        svg_avatar = INITIALS_SVG_TEMPLATE.format(**{
            'color1': f"#{random.randint(100000, 999999)}",
            'color2': f"#{random.randint(100000, 999999)}",
            'text_color': f"#{random.randint(100000, 999999)}",
            'text': xml_escape(initials.upper()),
        }).replace('\n', '')

        svg2png(svg_avatar, write_to=f"{settings.MEDIA_ROOT}/{instance.username}_default_avatar.png")
        instance.avatar = f"{instance.username}_default_avatar.png"
        instance.save()
