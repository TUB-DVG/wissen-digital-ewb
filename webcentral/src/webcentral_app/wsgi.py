"""
WSGI config for webcentral_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

import django
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import get_user_model


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webcentral_app.settings")
django.setup()

dotEnvSuperusername = os.environ["DJANGO_SUPERUSER_USERNAME"]
dotEnvSuperuserPassword = os.environ["DJANGO_SUPERUSER_PASSWORD"]
dotEnvSuperuserEmail = os.environ["DJANGO_SUPERUSER_EMAIL"]

User = get_user_model()

superusers = User.objects.filter(is_superuser=True)

correctSuperuserIsPresent = False
for superuser in superusers:
    if (
        superuser.username != dotEnvSuperusername
        or not superuser.check_password(dotEnvSuperuserPassword)
        or superuser.email != dotEnvSuperuserEmail
    ):
        superuser.delete()
    else:
        correctSuperuserIsPresent = True

if not correctSuperuserIsPresent:
    User.objects.create_superuser(
        dotEnvSuperusername, dotEnvSuperuserEmail, dotEnvSuperuserPassword
    )

application = get_wsgi_application()
