from django.contrib.auth.models import User
from django.db import models
from gcm.models import AbstractDevice


class UserDevice(AbstractDevice):

    user = models.ForeignKey(User, related_name='devices')

    def __unicode__(self):
        return u"%s %s" % (self.user, self.dev_id)
