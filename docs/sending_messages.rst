Sending messages
================

You can simply use the console

.. code-block:: bash

    $ python manage.py gcm_messenger --devices
    Devices list:
    (#1) My phone

    # python manage.py gcm_messagner <device_id> <message>
    $ python manage.py gcm_messenger 1 'my test message'

or django orm for that::

    from gcm.models import get_device_model
    my_phone = get_device_model().objects.get(name='My phone')
    my_phone.send_message('my test message')
