# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
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
        device.is_active = True
        device.save()
        return HttpResponse()

    return HttpResponseNotFound()

@csrf_exempt
def unregister(request):
    device_id = request.POST.get('device_id', None)
    if device_id is not None:
        device = get_object_or_404(Device, dev_id=device_id,)
        if device.is_active:
            device.is_active = False
            device.save()
            return HttpResponse()

    return HttpResponseNotFound()
