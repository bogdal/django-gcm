from django.core.urlresolvers import reverse
from gcm.models import Device
from tastypie.test import ResourceTestCase


class DeviceResourceTest(ResourceTestCase):

    def setUp(self):
        super(DeviceResourceTest, self).setUp()
        self.api_register_url = reverse("register-device", kwargs={'resource_name': 'device', 'api_name': 'v1'})
        self.api_unregister_url = reverse("unregister-device", kwargs={'resource_name': 'device', 'api_name': 'v1'})

    def _not_allowed_methods(self, url):
        self.assertHttpMethodNotAllowed(self.api_client.get(url))
        self.assertHttpMethodNotAllowed(self.api_client.put(url))
        self.assertHttpMethodNotAllowed(self.api_client.delete(url))

    def test_register_device_not_allowed_methods(self):
        self._not_allowed_methods(self.api_register_url)

    def test_unregister_device_not_allowed_methods(self):
        self._not_allowed_methods(self.api_unregister_url)

    def test_register_device(self):
        device_id = 'TEST001'
        data = {
            'dev_id': device_id,
            'reg_id': 'abcd1234',
        }
        response = self.api_client.post(self.api_register_url, data=data)
        self.assertHttpOK(response)

        devices = Device.objects.filter(dev_id=device_id)
        self.assertEqual(devices.count(), 1)
        self.assertTrue(list(devices).pop().is_active)

    def test_register_device_without_id(self):
        response = self.api_client.post(self.api_register_url, data={})
        self.assertHttpBadRequest(response)

    def test_update_registration_id(self):
        device_id = 'TEST'
        expected_registration_id = 'xyz1'
        device = Device.objects.create(dev_id=device_id, reg_id='abc1')

        data = {
            'dev_id': device_id,
            'reg_id': expected_registration_id
        }
        response = self.api_client.post(self.api_register_url, data=data)
        self.assertHttpOK(response)

        reg_id = Device.objects.get(pk=device.pk).reg_id
        self.assertEqual(reg_id, expected_registration_id)
