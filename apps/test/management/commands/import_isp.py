from django.core.management import BaseCommand
import json

from config.settings import BASE_DIR
from apps.setup.models import Country
from apps.test.models import Isp



class Command(BaseCommand):
    help = 'Your help message for this command'

    def handle(self, *args, **options):
        json_file_path = BASE_DIR / 'isp.json'

        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for isp_data in data:
            isp, created = Isp.objects.get_or_create(
                name=isp_data['name'],
                defaults={
                    'url': isp_data['url'],
                    'cloud': isp_data['cloud'],
                    'country': Country.objects.get_or_create(name=isp_data['country'])[0] if isp_data['country'] else None
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added ISP `{isp.name}`'))
            else:
                self.stdout.write(self.style.WARNING(f'ISP `{isp.name}` already exists'))
