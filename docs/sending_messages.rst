Sending messages
================

You can simply use the console:

.. code-block:: bash

    # Get the list of devices
    $ python manage.py gcm_messenger --devices
    > Devices list:
    > (#1) My phone

    # python manage.py gcm_messenger <device_id> <message> [--collapse-key <key>]
    $ python manage.py gcm_messenger 1 'my test message'

or django orm for that::

    from gcm.models import get_device_model

    my_phone = get_device_model().objects.get(name='My phone')
    my_phone.send_message('my test message', collapse_key='something')

In the above methods, ``collapse_key`` parameter is optional (default `message`).

.. _Lifetime of a Message: http://developer.android.com/google/gcm/adv.html

.. note:: For more information, see `Lifetime of a Message`_ docs.
