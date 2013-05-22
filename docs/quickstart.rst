Quickstart
==========

#. Install django-gcm

   .. code-block:: bash

      $ pip install django-gcm

#. Add the api resources to your URL router::

      # urls.py
      from django.conf.urls import include, patterns, url

      urlpatterns = patterns('',
          # ...
          url(r'', include('gcm.urls')),
      )

#. Configure your ``settings.py``::

      # settings.py
      INSTALLED_APPS = [
          # ...
          'gcm',
      ]

      GCM_APIKEY = "<api_key>"

