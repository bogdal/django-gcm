import requests
import json

from django.core.exceptions import ImproperlyConfigured

from . import conf


class GCMMessage(object):

    def __init__(self):
        self.api_key = conf.GCM_APIKEY

        if not self.api_key:
            raise ImproperlyConfigured(
                "You haven't set the 'GCM_APIKEY' setting yet.")

    def _chunks(self, items, limit):
        """
        Yield successive chunks from list \a items with a minimum size \a limit
        """
        for i in range(0, len(items), limit):
            yield items[i:i + limit]

    def send(self, regs_id, data, **kwargs):
        """
        Send a GCM message for one or more devices, using json data
        regs_id: A list with the devices which will be receiving a message
        data: The dict data which will be send
        Optional params e.g.:
            collapse_key: A string to group messages
        For more info see the following documentation:
        https://developer.android.com/google/gcm/server-ref.html#send-downstream
        """

        if not isinstance(data, dict):
            data = {'msg': data}

        if len(regs_id) > conf.GCM_MAX_RECIPIENTS:
            ret = []
            for chunk in self._chunks(regs_id, conf.GCM_MAX_RECIPIENTS):
                ret.append(self.send(chunk, data, **kwargs))
            return ret

        values = {
            'registration_ids': regs_id,
            'data': data,
            'collapse_key': 'message'}
        values.update(kwargs)

        values = json.dumps(values)

        headers = {
            'UserAgent': "GCM-Server",
            'Content-Type': 'application/json',
            'Authorization': 'key=' + self.api_key}

        response = requests.post(url="https://android.googleapis.com/gcm/send",
                                 data=values,
                                 headers=headers)
        response.raise_for_status()
        return regs_id, json.loads(response.content)
