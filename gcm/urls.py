from django.conf.urls.defaults import *

urlpatterns = patterns('gcm.views',
    url(r'^gcm/register/$', 'register', name='register-device'),
)
