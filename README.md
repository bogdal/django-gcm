django-gcm
==========
[![Build Status](https://travis-ci.org/bogdal/django-gcm.png?branch=master)](https://travis-ci.org/bogdal/django-gcm)

Google Cloud Messaging Server in Django

Quickstart
-------

Install the package via ``pip``

    pip install git+git://github.com/bogdal/django-gcm.git
    
Add <code>gcm</code> to <code>INSTALLED_APPS</code> in <code>settings.py</code>

Add <code>gcm urls</code> to <code>urls.py</code> file:

```python
  urlpatterns = patterns('',
      ...
      url(r'', include('gcm.urls')),
      ...
  )
```

