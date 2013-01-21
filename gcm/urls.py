from django.conf.urls import patterns, url


urlpatterns = patterns(
    'gcm.views',
    url(r'^gcm/register/$', 'register', name='register-device'),
)
