from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from . import conf
from . import api
from .utils import load_object


def get_device_model():
    return load_object(conf.GCM_DEVICE_MODEL)


class GCMMessage(api.GCMMessage):
    GCM_INVALID_ID_ERRORS = [u'InvalidRegistration',
                             u'NotRegistered',
                             u'MismatchSenderId']

    def send(self, regs_id, data, collapse_key=None):
        response = super(GCMMessage, self).send(regs_id, data, collapse_key)
        chunks = [response] if not isinstance(response, list) else response
        for chunk in chunks:
            self.post_send(*chunk)
        return response

    def post_send(self, regs_id, response):
        if response['failure']:
            invalid_messages = dict(filter(lambda x: x[1].get('error') in self.GCM_INVALID_ID_ERRORS,
                                           zip(regs_id, response.get('results'))))

            for device in get_device_model().objects.filter(reg_id__in=invalid_messages.keys()):
                device.mark_inactive(error_message=invalid_messages[device.reg_id]['error'])


class DeviceQuerySet(QuerySet):

    def send_message(self, data, collapse_key="message"):
        if self:
            return GCMMessage().send(
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

    def send_message(self, data, collapse_key="message"):
        return GCMMessage().send(
            regs_id=[self.reg_id],
            data=data,
            collapse_key=collapse_key)

    def mark_inactive(self, **kwargs):
        self.is_active = False
        self.save()


class Device(AbstractDevice):
    pass
