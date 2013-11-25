from django.conf.urls import patterns, include, url
from tastypie.api import Api
from .resources import AuthResource

gcm_api = Api(api_name='v1')
gcm_api.register(AuthResource())


urlpatterns = patterns('',
    url(r'^gcm/', include(gcm_api.urls)),
)
