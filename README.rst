django-gcm
==========

.. image:: https://travis-ci.org/bogdal/django-gcm.png?branch=master
    :target: https://travis-ci.org/bogdal/django-gcm

.. image:: https://coveralls.io/repos/bogdal/django-gcm/badge.png?branch=master
    :target: https://coveralls.io/r/bogdal/django-gcm?branch=master
    
.. image:: https://version-image.appspot.com/pypi/?name=django-gcm
    :target: https://pypi.python.org/pypi/django-gcm/
    

Google Cloud Messaging Server in Django

Quickstart
----------

Install the package via ``pip``::

    pip install django-gcm
    
Add ``gcm`` to ``INSTALLED_APPS`` in ``settings.py``

Add ``GCM_APIKEY`` to ``settings.py`` file:

.. code-block:: python

    GCM_APIKEY = "<api_key>"


Add ``gcm urls`` to ``urls.py`` file:

.. code-block:: python

    urlpatterns = patterns('',
      ...
      url(r'', include('gcm.urls')),
      ...
    )


Documentation: `https://django-gcm.readthedocs.org <https://django-gcm.readthedocs.org>`_


Client
------

Simple client application you can find `here <https://github.com/bogdal/pager>`_.
