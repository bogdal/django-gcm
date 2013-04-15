import urllib2
import json


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

    request = urllib2.Request("https://android.googleapis.com/gcm/send", data=values, headers=headers)
    response = urllib2.urlopen(request)
    result = response.read()

    return result
