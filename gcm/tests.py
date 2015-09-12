from __future__ import unicode_literals
import json
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from django.contrib.auth import get_user_model
from django.core import management
from django.core.exceptions import ImproperlyConfigured
from django.core.management import CommandError
from django.core.urlresolvers import reverse
from django.test import TestCase
from tastypie.test import ResourceTestCase
from mock import patch, PropertyMock, MagicMock
import requests

from . import conf
from .models import get_device_model
from .api import GCMMessage as ApiGCMMessage

Device = get_device_model()
User = get_user_model()


class CommandTest(TestCase):

    def test_gcm_urls(self):
        out = StringIO()
        management.call_command('gcm_urls', stdout=out)
        self.assertIn('/gcm/v1/device/register', out.getvalue())
        self.assertIn('/gcm/v1/device/unregister', out.getvalue())

    @patch.object(ApiGCMMessage, 'send')
    def test_send_message(self, mock_send):
        device_name = 'My test device'
        device = Device.objects.create(dev_id='device_1', name=device_name,
                                       reg_id='000123abc001', is_active=True)

        mock_send.return_value = (
            Device.objects.values_list('reg_id', flat=True),
            {'failure': 0, 'canonical_ids': 0, 'success': 1,
             'multicast_id': 112233, 'results': [{'message_id': '0:123123'}]})

        out = StringIO()
        management.call_command('gcm_messenger', device.id, 'test', stdout=out)
        self.assertTrue(mock_send.called)

        management.call_command('gcm_messenger', devices=True, stdout=out)
        self.assertIn(device_name, out.getvalue())

        self.assertRaises(
            CommandError, management.call_command, 'gcm_messenger')
        self.assertRaises(
            CommandError, management.call_command,
            'gcm_messenger', '999', 'test')


class AdminTest(TestCase):

    def setUp(self):
        user_password = 'password'
        user = User.objects.create_superuser(
            'admin', 'admin@test.com', user_password)
        self.client.login(username=user.username, password=user_password)

    @patch.object(ApiGCMMessage, 'send')
    def test_send_message(self, mock_send):
        device = Device.objects.create(
            dev_id='device_1', reg_id='000123abc001', is_active=True)

        mock_send.return_value = (
            Device.objects.values_list('reg_id', flat=True),
            {'failure': 0, 'canonical_ids': 0, 'success': 1,
             'multicast_id': 112233, 'results': [{'message_id': '0:123123'}]})

        self.client.post('/admin/gcm/device/',
                         data={'action': 'send_message_action',
                               '_selected_action': device.id})

        response = self.client.post('/admin/gcm/device/send-message/',
                                    data={'message': 'admin test message'})

        self.assertTrue(mock_send.called)
        self.assertEqual(response.status_code, 302)

    def test_do_not_send_empty_message(self):
        device = Device.objects.create(
            dev_id='device_1', reg_id='000123abc001', is_active=True)

        self.client.post('/admin/gcm/device/',
                         data={'action': 'send_message_action',
                               '_selected_action': device.id})

        response = self.client.post('/admin/gcm/device/send-message/')
        self.assertEqual(response.status_code, 200)

    def test_send_message_view_requires_devices(self):
        response = self.client.get('/admin/gcm/device/send-message/')
        self.assertRedirects(response, '/admin/gcm/device/')


class DeviceResourceTest(ResourceTestCase):

    def setUp(self):
        super(DeviceResourceTest, self).setUp()
        url_kwargs = {'resource_name': 'device', 'api_name': 'v1'}
        self.api_register_url = reverse(
            "register-device", kwargs=url_kwargs)
        self.api_unregister_url = reverse(
            "unregister-device", kwargs=url_kwargs)

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
        data = {'dev_id': device_id}
        Device.objects.create(dev_id=device_id, reg_id='abc1')
        response = self.api_client.post(self.api_unregister_url, data=data)
        self.assertHttpOK(response)

        devices = Device.objects.filter(dev_id=device_id)
        self.assertEqual(devices.count(), 1)
        self.assertFalse(list(devices).pop().is_active)

    def test_cannot_unregister_non_existent_device(self):
        device_id = 'FAKE_DEVICE_ID'
        data = {'dev_id': device_id}
        response = self.api_client.post(self.api_unregister_url, data=data)
        self.assertHttpBadRequest(response)
        self.assertEqual(Device.objects.all().count(), 0)

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
        Device.objects.create(
            dev_id='device_1', reg_id='000123abc001', is_active=True)
        Device.objects.create(
            dev_id='device_2', reg_id='000123abc002', is_active=True)
        Device.objects.create(
            dev_id='device_3', reg_id='000123abc003', is_active=True)

        mock_send.return_value = (
            Device.objects.values_list('reg_id', flat=True),
            {'failure': 2, 'canonical_ids': 0, 'success': 1,
             'multicast_id': 112233, 'results': [
                 {'error': 'InvalidRegistration'},
                 {'message_id': '0:123123'},
                 {'error': 'NotRegistered'}]})

        Device.objects.all().send_message('test message')

        devices = Device.objects.filter(is_active=False)
        self.assertEqual(devices.count(), 2)

    @patch.object(ApiGCMMessage, 'send')
    def test_ignore_unhandled_error(self, mock_send):
        Device.objects.create(
            dev_id='device_1', reg_id='000123abc001', is_active=True)

        mock_send.return_value = (
            Device.objects.values_list('reg_id', flat=True),
            {'failure': 1, 'canonical_ids': 0, 'success': 0,
             'multicast_id': 112233, 'results': [{'error': 'UnhandledError'}]})

        Device.objects.all().send_message('test message')

        device = Device.objects.get(dev_id='device_1')
        self.assertTrue(device.is_active)

    @patch.object(ApiGCMMessage, 'send')
    def test_ignore_active_device(self, mock_send):
        dev_id = 'device_1'
        device = Device.objects.create(
            dev_id=dev_id, reg_id='000123abc001', is_active=True)

        mock_send.return_value = (
            Device.objects.values_list('reg_id', flat=True),
            {'failure': 0, 'canonical_ids': 0, 'success': 1,
             'multicast_id': 112233, 'results': [{'message_id': '0:123123'}]})

        device.send_message('test message')
        self.assertEqual(str(Device.objects.get(is_active=True)), dev_id)

    @patch('requests.post')
    def test_send_message_to_topic(self, mocked_post):
        post = MagicMock()
        post.content = '{}'
        post.status_code = 200
        mocked_post.return_value = post
        gcm_message = ApiGCMMessage()
        message = 'test message'
        topic = '/topics/test-topic'
        gcm_message.send(message, to=topic)
        expected_data = {
            'data': {'msg': message},
            'to': topic,
            'collapse_key': 'message'}
        self.assertDictEqual(
            json.loads(mocked_post.call_args[1]['data']), expected_data)

    @patch.object(ApiGCMMessage, 'send')
    def test_ignore_empty_queryset(self, mock_send):
        Device.objects.all().send_message('test')
        self.assertFalse(mock_send.called)

    @patch.object(conf, 'GCM_MAX_RECIPIENTS',
                  new_callable=PropertyMock(return_value=2))
    def test_split_to_chunks(self, mock_max_recipients):

        Device.objects.create(
            dev_id='device_1', reg_id='000123abc001', is_active=True)
        Device.objects.create(
            dev_id='device_2', reg_id='000123abc002', is_active=True)

        Device.objects.create(
            dev_id='device_3', reg_id='000123abc003', is_active=True)
        Device.objects.create(
            dev_id='device_4', reg_id='000123abc004', is_active=True)

        Device.objects.create(
            dev_id='device_5', reg_id='000123abc005', is_active=True)

        chunk_messages = [
            {'failure': 1, 'canonical_ids': 0, 'success': 0,
             'multicast_id': '0003', 'results': [{'error': 'NotRegistered'}]},
            {'failure': 1, 'canonical_ids': 0, 'success': 1,
             'multicast_id': '0002', 'results': [
                 {'message_id': '0:123123'},
                 {'error': 'InvalidRegistration'}]},
            {'failure': 1, 'canonical_ids': 0, 'success': 1,
             'multicast_id': '0001', 'results': [
                 {'error': 'InvalidRegistration'},
                 {'message_id': '0:123123'}]}]

        def side_effect(**kwargs):
            mock = MagicMock()
            mock.content = json.dumps(chunk_messages.pop())
            return mock

        with patch.object(requests, 'post', side_effect=side_effect):
            Device.objects.all().send_message('test message')

        devices = Device.objects.filter(is_active=False)
        self.assertEqual(devices.count(), 3)

    @patch.object(conf, 'GCM_APIKEY',
                  new_callable=PropertyMock(return_value=None))
    def test_configuration(self, mock_apikey):
        device = Device.objects.create(
            dev_id='device_1', reg_id='000123abc001', is_active=True)
        self.assertRaises(
            ImproperlyConfigured, device.send_message, data='test')
