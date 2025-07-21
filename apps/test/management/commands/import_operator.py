from django.core.management.base import BaseCommand
import json
import os

from config.settings import BASE_DIR
from apps.setup.models import  Country
from apps.test.models import Operator

class Command(BaseCommand):
    help = 'وارد کردن اپراتورها از فایل JSON به دیتابیس'

    def handle(self, *args, **options):
        file_path = BASE_DIR / 'Operator.json'

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"فایل {file_path} پیدا نشد."))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            country_name = item.get('country')
            country, _ = Country.objects.get_or_create(name=country_name)

            operator, created = Operator.objects.get_or_create(
                name=item['name'],
                defaults={
                    'url': item.get('url', ''),
                    'isp': item.get('isp', ''),
                    'org': item.get('org', ''),
                    'country': country,
                    'as_number': item.get('as', ''),
                    'asname': item.get('asname', ''),
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"اپراتور '{operator.name}' با موفقیت ایجاد شد."))
            else:
                self.stdout.write(self.style.WARNING(f"اپراتور '{operator.name}' قبلاً وجود دارد."))

        self.stdout.write(self.style.SUCCESS("وارد کردن اپراتورها به پایان رسید."))
