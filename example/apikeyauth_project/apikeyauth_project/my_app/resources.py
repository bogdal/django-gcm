from gcm.resources import DeviceResource
from tastypie.authentication import ApiKeyAuthentication


class AuthResource(DeviceResource):

    class Meta(DeviceResource.Meta):
        authentication = ApiKeyAuthentication()

    def get_queryset(self):
        qs = super(AuthResource, self).get_queryset()
        # to make sure that user can update only his own devices
        return qs.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AuthResource, self).form_valid(form)
