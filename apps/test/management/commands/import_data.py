from django.core.management.base import BaseCommand
import json
import os

from config.settings import BASE_DIR
from apps.test.models import SpeedTest


class Command(BaseCommand):
    help = 'Import speed test data from JSON file into the database'

    def handle(self, *args, **options):
        file_path = BASE_DIR / 'test_speedtest.json'

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File '{file_path}' not found."))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        created_count = 0
        for item in data:
            # Remove the ID if it's in the data

            SpeedTest.objects.create(
                ping_avg=item['ping_avg'],
                jitter=item['jitter'],
                packet_loss=item['packet_loss'],
                speed_mbps=item['speed_mbps'],
                loaded_size=item['loaded_size'],
                load_time=item['load_time'],
                upload_speed_mbps=item['upload_speed_mbps'],
                upload_time=item['upload_time'],
                upload_file_size=item['upload_file_size'],
                latency=item['latency'],
                test_state=item['test_state'],
                date=item['date'],
                device_info_id=item['device_info_id'],
                network_info_id=item['network_info_id'],
                user_id=item['user_id'],
                server_test_id=item['server_test_id'],
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"SpeedTest entry #{created_count} created."))

        self.stdout.write(self.style.SUCCESS(f"Import finished. {created_count} new records added."))
