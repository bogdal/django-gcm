from tastypie.authentication import ApiKeyAuthentication
from gcm.resources import DeviceResource


class CustomResource(DeviceResource):

    class Meta(DeviceResource.Meta):
        authentication = ApiKeyAuthentication()

    def get_queryset(self):
        qs = super(CustomResource, self).get_queryset()
        return qs.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CustomResource, self).form_invalid(form)
