from django.conf.urls import patterns, url, include
from tastypie.api import Api

from .resources import DeviceResource

gcm_api = Api(api_name='v1')
gcm_api.register(DeviceResource())


urlpatterns = patterns('', url(r'^gcm/', include(gcm_api.urls)))
