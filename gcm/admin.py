from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from gcm.models import Device


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['dev_id', 'name', 'modified_date', 'is_active']
    search_fields = ('dev_id', 'name')
    list_filter = ['is_active']
    date_hierarchy = 'modified_date'
    readonly_fields = ('dev_id', 'reg_id')
    actions = ['send_test_message']

    def send_test_message(self, request, queryset):
        for device in queryset:
            device.send_message('GCM: Test message')
        self.message_user(request, _("All messages were sent."))
    send_test_message.short_description = _("Send test message")


admin.site.register(Device, DeviceAdmin)