from .base import *


DEBUG = False

ALLOWED_HOSTS = ["*"]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'storage/static'),
)


# Media files/user's files
MEDIA_ROOT = 'storage/media'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_USE_TLS = True
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'foo@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'very_secret_password')
EMAIL_SENDER = 'DjangoBoards Develop Team'
