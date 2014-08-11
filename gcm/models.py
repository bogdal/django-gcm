from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from . import conf
from .api import send_gcm_message
from .utils import load_object


def get_device_model():
    return load_object(conf.GCM_DEVICE_MODEL)


def get_api_key():
    if not conf.GCM_APIKEY:
        raise ImproperlyConfigured("You haven't set the 'GCM_APIKEY' setting yet.")
    return conf.GCM_APIKEY


class DeviceQuerySet(QuerySet):

    def send_message(self, data, collapse_key="message"):
        if self:
            return send_gcm_message(
                api_key=get_api_key(),
                regs_id=list(self.values_list("reg_id", flat=True)),
                data=data,
                collapse_key=collapse_key)


class DeviceManager(models.Manager):

    def get_queryset(self):
        return DeviceQuerySet(self.model)
    get_query_set = get_queryset  # Django < 1.6 compatiblity


class AbstractDevice(models.Model):

    dev_id = models.CharField(max_length=50, verbose_name=_("Device ID"), unique=True)
    reg_id = models.CharField(max_length=255, verbose_name=_("Registration ID"), unique=True)
    name = models.CharField(max_length=255, verbose_name=_("Name"), blank=True, null=True)
    creation_date = models.DateTimeField(verbose_name=_("Creation date"), auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name=_("Modified date"), auto_now=True)
    is_active = models.BooleanField(verbose_name=_("Is active?"), default=False)

    objects = DeviceManager()

    def __unicode__(self):
        return self.dev_id

    class Meta:
        abstract = True
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")
        ordering = ['-modified_date']

    def send_message(self, msg, collapse_key="message"):
        if isinstance(msg, dict):
            data = msg
        else:
            data = {'msg': msg}

        return send_gcm_message(
            api_key=get_api_key(),
            regs_id=[self.reg_id],
            data=data,
            collapse_key=collapse_key)


class Device(AbstractDevice):
    pass
