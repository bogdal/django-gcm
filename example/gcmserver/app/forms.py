from gcm.forms import DeviceForm as GcmDeviceForm


class DeviceForm(GcmDeviceForm):

    def __init__(self, user, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super(DeviceForm, self).save(commit=True)
        if not self.user.devices.filter(device=instance).exists():
            self.user.devices.create(device=instance)
        return instance
