from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from gcm.models import Device


class Command(BaseCommand):
    args = '<device_id message>'
    help = 'Send message through gcm api'

    option_list = BaseCommand.option_list + (
        make_option(
            '--devices',
            action='store_true',
            dest='devices',
            default=False,
            help='List of available devices'),)

    def handle(self, *args, **options):

        if options['devices']:
            devices = Device.objects.filter(is_active=True)

            self.stdout.write("Devices list:\n")
            for device in devices:
                self.stdout.write("(#%s) %s\n" % (device.id, device.name))
            self.stdout.write("\n")
        else:

            try:
                id = args[0]
                message = args[1]
            except IndexError:
                raise CommandError(
                    "Invalid params. You have to put all params: python manage.py messanger <device_id> <msg>")

            try:
                device = Device.objects.get(pk=int(id), is_active=True)
            except Device.DoesNotExist:
                raise CommandError('Unknown device (id=%s). Check list: python manage.py messenger --devices' % id)
            else:
                result = device.send_message(message)

                self.stdout.write("[OK] device #%s (%s): %s\n" % (id, device.name, result))
