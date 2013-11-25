from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import Resource
from tastypie.serializers import Serializer

from . import signals
from .forms import RegisterDeviceForm, UnregisterDeviceForm
from .models import get_device_model


class DeviceResource(Resource):

    DEVICE_ID_FIELD_NAME = 'dev_id'

    model_class = get_device_model()
    register_form_class = RegisterDeviceForm
    unregister_form_class = UnregisterDeviceForm
    object = None
    request = None

    class Meta:
        resource_name = 'device'
        allowed_methods = ['post']
        authentication = Authentication()
        authorization = Authorization()
        serializer = Serializer(formats=['json'])

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/register/$" %
                self._meta.resource_name, self.wrap_view('register'),
                name="register-device"),
            url(r"^(?P<resource_name>%s)/unregister/$" %
                self._meta.resource_name, self.wrap_view('unregister'),
                name="unregister-device"),
        ]

    def _verify(self, request):
        self.is_authenticated(request)
        self.throttle_check(request)
        self.method_check(request, self._meta.allowed_methods)

    def get_form_kwargs(self):
        data = self.deserialize(self.request, self.request.body)
        kwargs = {'data': data}
        try:
            kwargs['instance'] = self.get_instance(data)
        except ObjectDoesNotExist:
            pass
        return kwargs

    def get_form(self, form_class):
        return form_class(**self.get_form_kwargs())

    def get_queryset(self):
        return self.model_class.objects.all()

    def get_instance(self, data):
        kwargs = {self.DEVICE_ID_FIELD_NAME:
                  data.get(self.DEVICE_ID_FIELD_NAME)}
        return self.get_queryset().get(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse

    def form_invalid(self, form):
        return HttpResponseBadRequest

    def _form_processing(self, form_class, request):
        self._verify(request)
        self.request = request

        form = self.get_form(form_class)

        if form.is_valid():
            response_class = self.form_valid(form)
        else:
            response_class = self.form_invalid(form)

        return self.create_response(request, data={},
                                    response_class=response_class)

    def register(self, request, **kwargs):
        form_class = self.register_form_class
        response = self._form_processing(form_class, request)
        signals.device_registered.send(sender=self, device=self.object,
                                       request=request)
        return response

    def unregister(self, request, **kwargs):
        form_class = self.unregister_form_class
        response = self._form_processing(form_class, request)
        signals.device_unregistered.send(sender=self, device=self.object,
                                         request=request)
        return response
