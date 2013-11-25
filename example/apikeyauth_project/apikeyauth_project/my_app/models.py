from django.conf import settings
from django.db import models
from gcm.models import AbstractDevice


class MyDevice(AbstractDevice):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
