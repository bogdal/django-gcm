from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # resources with api key authentication
    url(r'^my/', include('gcmserver.app.urls')),

    # basic resources without authentication
    url(r'', include('gcm.urls')),
)
