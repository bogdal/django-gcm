from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from gcm.models import Device


class GcmTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_device(self):
        device_id = 'TEST001'
        data = {
            'device_id': device_id,
            'reg_id': 'abcdefghijklm',
        }

        self.client.post(reverse("register-device"), data=data)

        results = Device.objects.filter(dev_id=device_id)
        self.assertEqual(results.count(), 1)
