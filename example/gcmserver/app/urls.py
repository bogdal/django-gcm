from django.conf.urls import patterns, include, url
from tastypie.api import Api

from .resources import CustomResource


gcm_api = Api(api_name='v1')
gcm_api.register(CustomResource())

urlpatterns = patterns('',
    url(r'^gcm/', include(gcm_api.urls)),
)
