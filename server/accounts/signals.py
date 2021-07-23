import cairosvg

from django.core.files.base import ContentFile

from accounts.utils import get_svg_avatar


def generate_avatar(sender, instance, created, **kwargs):
    if not created:
        initials = instance.initials
        initial_avatar_name = f'u{instance.pk}pk_{initials}_.png'
        if not instance.avatar and initials:
            svg_avatar = get_svg_avatar(initials)
            avatar = ContentFile(cairosvg.svg2png(svg_avatar))
            instance.avatar.save(initial_avatar_name, avatar)
        elif instance.avatar and f'u{instance.pk}pk_' in instance.avatar.name:
            if f'_{initials}_' not in instance.avatar.name or not initials:
                instance.avatar.delete()
