from .base import *


DEBUG = True

ALLOWED_HOSTS = ["*"]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'storage/static'),
)


# Media files/user's files
MEDIA_ROOT = 'storage/media'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'foo@gmail.com')
