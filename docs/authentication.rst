Api key authentication
======================

Allows you to manage access to the GCM api using one of the available ``tastypie`` authentication method - `ApiKeyAuthentication`.

.. _django-tastypie Authentication: http://django-tastypie.readthedocs.org/en/latest/authentication.html

.. note:: I strongly recommend see `django-tastypie Authentication`_ docs.


Adding authentication requires `tastypie` added to your `INSTALLED_APPS` in the ``settings.py`` file:

.. code-block:: python

    INSTALLED_APPS = [
          ...
          'gcm',
          'tastypie',
      ]


Adding user field
--------------

You need to extend `Device` model and add user field. (See :ref:`extending_device`)

.. code-block:: python

    # your_app/models.py
    from django.conf import settings
    from django.db import models
    from gcm.models import AbstractDevice

    class MyDevice(AbstractDevice):

        user = models.ForeignKey(settings.AUTH_USER_MODEL)


Add appropriate path to the ``settings.py`` file:

.. code-block:: python

    GCM_DEVICE_MODEL = 'your_app.models.MyDevice'


Resource class
--------------

In your application, you need to create your own Resource class. It has to inherit from `gcm.resources.DeviceResource`.


.. code-block:: python

    # your_app/resources.py
    from gcm.resources import DeviceResource
    from tastypie.authentication import ApiKeyAuthentication

    class AuthResource(DeviceResource):

        class Meta(DeviceResource.Meta):
            authentication = ApiKeyAuthentication()

        def get_queryset(self):
            qs = super(AuthResource, self).get_queryset()
            # to make sure that user can update only his own devices
            return qs.filter(user=self.request.user)

        def form_valid(self, form):
            form.instance.user = self.request.user
            return super(AuthResource, self).form_valid(form)



You need to hook your resource class up in your ``urls.py`` file:

.. code-block:: python

    # your_app/urls.py
    from django.conf.urls import patterns, include, url
    from tastypie.api import Api
    from .resources import AuthResource

    gcm_api = Api(api_name='v1')
    gcm_api.register(AuthResource())


    urlpatterns = patterns('',
        url(r'^gcm/', include(gcm_api.urls)),
    )


Include your ``urls.py`` file to the main URL router:

.. code-block:: python

    # urls.py
    from django.conf.urls import include, patterns, url

    urlpatterns = patterns('',
        url(r'', include('your_app.urls')),
    )


.. note:: See an example project ``gcm/example/apikeyauth_project``


