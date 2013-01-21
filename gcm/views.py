# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from gcm.models import Device

@csrf_exempt
def register(request):
    """
    Register device

    Args:
        reg_id - reg id from android app
        device_id - unique device id
    """
    device_id = request.POST.get('device_id', None)
    if device_id is not None:
        device, created = Device.objects.get_or_create(dev_id=device_id)
        device.reg_id = request.POST.get('reg_id')
        device.save()

    return HttpResponse()

