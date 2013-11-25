Quickstart
==========

#. Install package via `pip`:

   .. code-block:: bash

      $ pip install django-gcm

#. Add `django-gcm` resources to your URL router::

      # urls.py
      from django.conf.urls import include, patterns, url

      urlpatterns = patterns('',
          url(r'', include('gcm.urls')),
      )


   To check gcm urls just use the following command:

   .. code-block:: bash

        $ python manage.py gcm_urls

        GCM urls:
        * Register device
            /gcm/v1/device/register/
        * Unregister device
            /gcm/v1/device/unregister/


#. Configure `django-gcm` in your ``settings.py`` file::

      INSTALLED_APPS = [
          # ...
          'gcm',
      ]

      GCM_APIKEY = "<api_key>"

.. note:: To obtain api key go to https://code.google.com/apis/console and grab the key for the server app.