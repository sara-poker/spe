from django.core.management import BaseCommand
import json

from config.settings import BASE_DIR
from apps.setup.models import Country



class Command(BaseCommand):
    help = 'ایمپورت  اطلاعات کشور ها به دیتابیس'

    def handle(self, *args, **options):
        json_file_path = BASE_DIR / 'countries.json'

        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for country_data in data:
            country, created = Country.objects.update_or_create(
                name=country_data['name'],
                defaults={
                    'country_id': country_data['country_id'],
                    'continent': country_data['continent'],
                    'population': country_data['population'],
                    'persian_name': country_data.get('persian_name', None)
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added country {country.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Country {country.name} already exists'))
