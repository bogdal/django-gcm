Device registration endpoints
=============================

Default ``django-gcm`` endpoints:

    * /gcm/v1/device/register/
    * /gcm/v1/device/unregister/

.. note:: Command ``python manage.py gcm_urls`` returns the current endpoints.

Register
--------

POST parameters:

``dev_id``
    Unique device identifier

``reg_id``
    Registration token

``name``
    Optional device name


.. code-block:: bash

    curl -X POST -H "Content-Type: application/json" -d '{"dev_id": "test", "reg_id":"abcd", "name":"test device"}' \
    http://localhost:8000/gcm/v1/device/register/

Unregister
----------

POST parameters:

``dev_id``
    Unique device identifier


.. code-block:: bash

    curl -X POST -H "Content-Type: application/json" -d '{"dev_id": "test"}' http://localhost:8000/gcm/v1/device/unregister/
