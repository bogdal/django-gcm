from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import get_device_model


class RegisterDeviceForm(forms.ModelForm):

    class Meta:
        model = get_device_model()
        fields = ('dev_id', 'reg_id',)

    def save(self, commit=True):
        self.instance.is_active = True
        return super(RegisterDeviceForm, self).save(commit)


class UnregisterDeviceForm(forms.ModelForm):

    class Meta:
        model = get_device_model()
        fields = ('dev_id',)

    def save(self, commit=True):
        self.instance.is_active = False
        return super(UnregisterDeviceForm, self).save(commit)


class MessageForm(forms.Form):

    message = forms.CharField(label=_('Message'), required=True)
