import json
from django.core.management.base import BaseCommand
from apps.test.models import Isp  # 👈 اسم دقیق اپت رو بذار اینجا

class Command(BaseCommand):
    help = "Import ISP data from JSON"

    def handle(self, *args, **kwargs):
        with open('test_isp.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            isp_obj, created = Isp.objects.update_or_create(
                name=item['name'],
                defaults={
                    'url': item.get('url', ''),
                    'isp': item['isp'],
                    'org': item['org'],
                    'as_number': item['as_number'],
                    'asname': item['asname'],
                    'cloud': item['cloud'].lower() == 'true',
                    'country_id': item['country_id']
                }
            )
            status = "Created" if created else "Updated"
            print(f"{status}: {isp_obj.name}")
