from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from gcm.models import get_device_model

Device = get_device_model()


class Command(BaseCommand):
    args = '<device_id message>'
    help = 'Send message through gcm api'

    def add_arguments(self, parser):
        parser.add_argument('device_id', nargs='?', type=int)
        parser.add_argument('message', nargs='?', type=str)
        parser.add_argument(
            '--devices',
            action='store_true',
            dest='devices',
            default=False,
            help='List of available devices'
        )
        parser.add_argument(
            '--collapse-key',
            dest='collapse_key',
            default='message',
            help='Set value of collapse_key flag, default is "message"'
        )

    def handle(self, *args, **options):

        if options.get('devices', False):
            devices = Device.objects.filter(is_active=True)

            self.stdout.write("Devices list:\n")
            for device in devices:
                self.stdout.write("(#%s) %s\n" % (device.id, device.name))
            self.stdout.write("\n")
        else:
            collapse_key = options.get('collapse_key', 'message')
            id = options.get('device_id')
            message = options.get('message')

            if not (id and message):
                raise CommandError(
                    "Invalid params. You have to put all params: "
                    "python manage.py gcm_messenger <device_id> <msg>")

            try:
                device = Device.objects.get(pk=int(id), is_active=True)
            except Device.DoesNotExist:
                raise CommandError(
                    'Unknown device (id=%s). Check list: '
                    'python manage.py gcm_messenger --devices' % id)
            else:
                result = device.send_message(
                        {'message': message}, collapse_key=collapse_key)

                self.stdout.write("[OK] device #%s (%s): %s\n" %
                                  (id, device.name, result))
