
import json
from django.core.management.base import BaseCommand
from apps.test.models import NetworkInfo  # مدل خودت رو بذار اینجا

class Command(BaseCommand):
    help = "Import user IP info from JSON"

    def handle(self, *args, **kwargs):
        with open('test_networkinfo.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            ip_obj, created = NetworkInfo.objects.update_or_create(
                ip=item['ip'],
                defaults={
                    'city': item['city'],
                    'country_id': item['country_id'],
                    'isp_id': item['isp_id']
                }
            )
            status = "Created" if created else "Updated"
            print(f"{status}: {ip_obj.ip} - {ip_obj.city}")
