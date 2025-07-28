import json
from django.core.management.base import BaseCommand
from apps.test.models import DeviceInfo  # 👈 مدل خودت رو بذار اینجا

class Command(BaseCommand):
    help = "Import client device info from JSON"

    def handle(self, *args, **kwargs):
        with open('test_deviceinfo.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            device_obj, created = DeviceInfo.objects.update_or_create(
                os=item['os'],
                os_version=item['os_version'],
                cpu=item['cpu'],
                browser=item['browser'],
                network_kind=item['network_kind'],
                device=item['device']
            )
            status = "Created" if created else "Exists"
            print(f"{status}: {device_obj.os} - {device_obj.browser}")
