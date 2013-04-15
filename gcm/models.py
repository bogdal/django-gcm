from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from gcm.api import send_gcm_message


class Device(models.Model):

    name = models.CharField(max_length=255, verbose_name=_("Name"), blank=True, null=True)
    dev_id = models.CharField(max_length=50, verbose_name=_("Device ID"), unique=True)
    reg_id = models.TextField(verbose_name=_("RegID"), blank=True, null=True)
    creation_date = models.DateTimeField(verbose_name=_("Creation date"), auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name=_("Modified date"), auto_now=True)
    is_active = models.BooleanField(verbose_name=_("Is active?"), default=False)

    def __unicode__(self):
        return self.dev_id

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")
        ordering = ['-modified_date']

    def send_message(self, msg):
        return send_gcm_message(
            api_key=settings.GCM_APIKEY,
            regs_id=[self.reg_id],
            data={'msg': msg},
            collapse_key="message")
