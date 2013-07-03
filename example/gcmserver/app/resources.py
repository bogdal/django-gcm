from tastypie.authentication import ApiKeyAuthentication
from gcm.resources import DeviceResource

from .forms import DeviceForm


class CustomResource(DeviceResource):

    class Meta(DeviceResource.Meta):
        authentication = ApiKeyAuthentication()

    def get_form_class(self, **kwargs):
        return DeviceForm(self.request.user, **kwargs)
