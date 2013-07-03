from django.contrib.auth.models import User
from django.db import models


class UserDevice(models.Model):

    user = models.ForeignKey(User, related_name='devices')
    device = models.OneToOneField('gcm.Device')

    def __unicode__(self):
        return u"%s %s" % (self.user, self.device.dev_id)
