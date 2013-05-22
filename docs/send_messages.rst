Send messages
=============

You can simply use the console:

.. code-block:: bash

    $ python manage.py gcm_messenger --devices
    Devices list:
    (#1) My phone
    
    $ python manage.py gcm_messenger 1 'my test message'
    [OK] device #1 (My phone): id=xxxxx

or use python for that::

    from gcm.models import Device
    my_phone = Device.objects.get(name='My phone')
    my_phone.send_message('my test message')
