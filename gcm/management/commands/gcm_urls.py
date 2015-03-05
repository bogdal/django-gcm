from django.core.management.base import NoArgsCommand
from django.core.urlresolvers import reverse


class Command(NoArgsCommand):
    help = "Show GCM urls"

    def show_line(self):
        self.stdout.write("%s\n" % ("-" * 30))

    def handle_noargs(self, **options):
        url_kwargs = {'resource_name': 'device', 'api_name': 'v1'}
        register_url = reverse("register-device", kwargs=url_kwargs)
        unregister_url = reverse("unregister-device", kwargs=url_kwargs)

        self.show_line()
        self.stdout.write("GCM urls:\n")
        self.stdout.write("* Register device\n    %s\n" % register_url)
        self.stdout.write("* Unregister device\n    %s\n" % unregister_url)
        self.show_line()
