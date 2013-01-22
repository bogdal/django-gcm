from django.http import HttpResponse, HttpResponseBadRequest
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import Resource
from tastypie.serializers import Serializer
from django.conf.urls import url
from gcm.forms import DeviceForm
from gcm.models import Device


class DeviceResource(Resource):

    class Meta:
        resource_name = 'device'
        allowed_methods = ['post']
        authentication = Authentication()
        authorization = Authorization()
        serializer = Serializer(formats=['json'])

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/register/$" % self._meta.resource_name,
                self.wrap_view('register'), name="register-device"),
            url(r"^(?P<resource_name>%s)/unregister/$" % self._meta.resource_name,
                self.wrap_view('unregister'), name="unregister-device"),
        ]

    def _verify(self, request):
        self.is_authenticated(request)
        self.throttle_check(request)
        self.method_check(request, self._meta.allowed_methods)

    def _form_processing(self, request, is_active):
        self._verify(request)

        kwargs = {
            'data': self.deserialize(request, request.raw_post_data)
        }
        try:
            kwargs['instance'] = Device.objects.get(dev_id=kwargs['data'].get('dev_id'))
        except Device.DoesNotExist:
            pass

        form = DeviceForm(**kwargs)
        self.response_class = HttpResponseBadRequest

        if form.is_valid():
            device = form.save(commit=False)
            device.is_active = is_active
            device.save()
            self.response_class = HttpResponse

    def register(self, request, **kwargs):
        self._form_processing(request, is_active=True)
        return self.create_response(request, data={}, response_class=self.response_class)

    def unregister(self, request, **kwargs):
        self._form_processing(request, is_active=False)
        return self.create_response(request, data={}, response_class=self.response_class)
