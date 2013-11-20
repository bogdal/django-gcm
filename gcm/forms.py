from django import forms

from .models import get_device_model


class DeviceForm(forms.ModelForm):
    class Meta:
        model = get_device_model()
        fields = ('dev_id', 'reg_id', 'is_active')
