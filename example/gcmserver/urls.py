from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # gcm
    url(r'^register/', 'gcm.views.device', name='register-device'),

    url(r'^admin/', include(admin.site.urls)),
)
