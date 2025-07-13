"""
ASGI config for RoyalStore project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RoyalStore.settings')

django_asgi_app = get_asgi_application()

from django.conf import settings
if not settings.DEBUG:
    from whitenoise import WhiteNoise

    django_asgi_app = WhiteNoise(django_asgi_app, root=settings.STATIC_ROOT)
    if os.path.isdir(settings.MEDIA_ROOT):
        django_asgi_app.add_files(settings.MEDIA_ROOT, prefix=settings.MEDIA_URL)

application = ProtocolTypeRouter({
    "http": django_asgi_app,
})
