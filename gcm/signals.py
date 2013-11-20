from django.dispatch import Signal

signal_args = ['device', 'request']

device_registered = Signal(providing_args=signal_args)
device_unregistered = Signal(providing_args=signal_args)
