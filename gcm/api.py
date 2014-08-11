import requests
import json

MAX_RECIPIENTS = 1000


def _chunks(items, limit):
    """
    Yield successive chunks from list \a items with a minimum size \a limit
    """
    for i in range(0, len(items), limit):
        yield items[i:i + limit]


def send_gcm_message(api_key, regs_id, data, collapse_key=None):
    """
    Send a GCM message for one or more devices, using json data
    api_key: The API_KEY from your console (https://code.google.com/apis/console, locate Key for Server Apps in
        Google Cloud Messaging for Android)
    regs_id: A list with the devices which will be receiving a message
    data: The dict data which will be send
    collapse_key: A string to group messages, look at the documentation about it:
        http://developer.android.com/google/gcm/gcm.html#request
    """

    if len(regs_id) > MAX_RECIPIENTS:
        ret = []
        for chunk in _chunks(regs_id, MAX_RECIPIENTS):
            ret.append(send_gcm_message(api_key, chunk, data, collapse_key))
        return ret

    values = {
        'registration_ids': regs_id,
        'collapse_key': collapse_key,
        'data': data
    }

    values = json.dumps(values)

    headers = {
        'UserAgent': "GCM-Server",
        'Content-Type': 'application/json',
        'Authorization': 'key=' + api_key,
    }

    response = requests.post(url="https://android.googleapis.com/gcm/send",
                             data=values,
                             headers=headers)
    response.raise_for_status()
    return json.loads(response.content)
