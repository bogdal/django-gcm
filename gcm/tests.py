import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from tastypie.test import ResourceTestCase
from mock import patch, PropertyMock, MagicMock
import requests

from . import conf
from .models import get_device_model
from .api import GCMMessage as ApiGCMMessage

Device = get_device_model()


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

    def test_unregister_device(self):
        device_id = 'TEST001'
        data = {
            'dev_id': device_id,
        }
        response = self.api_client.post(self.api_unregister_url, data=data)
        self.assertHttpOK(response)

        devices = Device.objects.filter(dev_id=device_id)
        self.assertEqual(devices.count(), 1)
        self.assertFalse(list(devices).pop().is_active)

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


class GCMMessageTest(TestCase):

    @patch.object(ApiGCMMessage, 'send')
    def test_mark_inactive(self, mock_send):
        Device.objects.create(dev_id='device_1', reg_id='000123abc001', is_active=True)
        Device.objects.create(dev_id='device_2', reg_id='000123abc002', is_active=True)
        Device.objects.create(dev_id='device_3', reg_id='000123abc003', is_active=True)

        mock_send.return_value = (Device.objects.values_list('reg_id', flat=True),
                                  {u'failure': 2, u'canonical_ids': 0, u'success': 1, u'multicast_id': 112233,
                                   u'results': [
                                       {u'error': u'InvalidRegistration'},
                                       {u'message_id': u'0:123123'},
                                       {u'error': u'NotRegistered'}]})

        Device.objects.all().send_message('test message')

        devices = Device.objects.filter(is_active=False)
        self.assertEqual(devices.count(), 2)

    @patch.object(ApiGCMMessage, 'send')
    def test_ignore_unhandled_error(self, mock_send):
        Device.objects.create(dev_id='device_1', reg_id='000123abc001', is_active=True)

        mock_send.return_value = (Device.objects.values_list('reg_id', flat=True),
                                  {u'failure': 1, u'canonical_ids': 0, u'success': 0, u'multicast_id': 112233,
                                   u'results': [{u'error': u'UnhandledError'}]})

        Device.objects.all().send_message('test message')

        device = Device.objects.get(dev_id='device_1')
        self.assertTrue(device.is_active)

    @patch.object(conf, 'GCM_MAX_RECIPIENTS', new_callable=PropertyMock(return_value=2))
    def test_split_to_chunks(self, mock_max_recipients):

        Device.objects.create(dev_id='device_1', reg_id='000123abc001', is_active=True)
        Device.objects.create(dev_id='device_2', reg_id='000123abc002', is_active=True)

        Device.objects.create(dev_id='device_3', reg_id='000123abc003', is_active=True)
        Device.objects.create(dev_id='device_4', reg_id='000123abc004', is_active=True)

        Device.objects.create(dev_id='device_5', reg_id='000123abc005', is_active=True)

        chunk_messages = [
            {u'failure': 1, u'canonical_ids': 0, u'success': 0, u'multicast_id': 0003,
             u'results': [{u'error': u'NotRegistered'}]},
            {u'failure': 1, u'canonical_ids': 0, u'success': 1, u'multicast_id': 0002,
             u'results': [{u'message_id': u'0:123123'}, {u'error': u'InvalidRegistration'}]},
            {u'failure': 1, u'canonical_ids': 0, u'success': 1, u'multicast_id': 0001,
             u'results': [{u'error': u'InvalidRegistration'}, {u'message_id': u'0:123123'}]}]

        def side_effect(**kwargs):
            mock = MagicMock()
            mock.content = json.dumps(chunk_messages.pop())
            return mock

        with patch.object(requests, 'post', side_effect=side_effect):
            Device.objects.all().send_message('test message')

        devices = Device.objects.filter(is_active=False)
        self.assertEqual(devices.count(), 3)
