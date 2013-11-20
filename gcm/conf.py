from django.conf import settings

GCM_DEVICE_MODEL = getattr(settings, 'GCM_DEVICE_MODEL', 'gcm.models.Device')
