from django import forms

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
