django-gcm
==========

.. image:: https://img.shields.io/travis/bogdal/django-gcm/master.svg
    :target: https://travis-ci.org/bogdal/django-gcm

.. image:: https://img.shields.io/codecov/c/github/bogdal/django-gcm/master.svg
    :target: https://codecov.io/github/bogdal/django-gcm?branch=master
    
.. image:: https://requires.io/github/bogdal/django-gcm/requirements.svg?branch=master
    :target: https://requires.io/github/bogdal/django-gcm/requirements/?branch=master

.. image:: https://img.shields.io/pypi/v/django-gcm.svg
    :target: https://pypi.python.org/pypi/django-gcm/
    

Google Cloud Messaging Server in Django

Quickstart
----------

Install the package via ``pip``::

    pip install django-gcm  --process-dependency-links
    
Add ``gcm`` to ``INSTALLED_APPS`` in ``settings.py``

Add ``GCM_APIKEY`` to ``settings.py`` file:

.. code-block:: python

    GCM_APIKEY = "<api_key>"


Add ``gcm urls`` to ``urls.py`` file:

.. code-block:: python

    urlpatterns = [
      ...
      url(r'', include('gcm.urls')),
      ...
    ]


Documentation: `https://django-gcm.readthedocs.org <https://django-gcm.readthedocs.org>`_


Client
------

Simple client application you can find `here <https://github.com/bogdal/pager>`_.
