from django import forms
from gcm.models import Device


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ('dev_id', 'reg_id', 'is_active')
