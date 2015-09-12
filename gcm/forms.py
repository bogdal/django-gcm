from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import get_device_model


class RegisterDeviceForm(forms.ModelForm):

    class Meta:
        model = get_device_model()
        fields = ('dev_id', 'reg_id', 'name',)

    def save(self, commit=True):
        self.instance.is_active = True
        return super(RegisterDeviceForm, self).save(commit)


class UnregisterDeviceForm(forms.ModelForm):

    class Meta:
        model = get_device_model()
        fields = ('dev_id',)

    def clean(self):
        if not self.instance.pk:
            raise forms.ValidationError(
                "Device '%s' does not exist" % self.cleaned_data['dev_id'])
        return self.cleaned_data

    def save(self, commit=True):
        self.instance.mark_inactive()
        return super(UnregisterDeviceForm, self).save(commit)


class MessageForm(forms.Form):

    message = forms.CharField(label=_('Message'), required=True)
