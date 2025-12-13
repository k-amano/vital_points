import json
from django.core.management.base import BaseCommand
from quiz.models import VitalPoint


class Command(BaseCommand):
    help = '急所マスターデータをJSONから読み込む'

    def handle(self, *args, **options):
        json_path = '/home/administrator/Projects/vital_points/vital_points_master.json'

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        VitalPoint.objects.all().delete()
        self.stdout.write('既存のデータを削除しました')

        count = 0
        for image_name, image_data in data.items():
            category = image_data['category']
            for point in image_data['points']:
                VitalPoint.objects.create(
                    number=point['number'],
                    name=point['name'],
                    reading=point['reading'],
                    category=category,
                    image_file=image_name
                )
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f'{count}件の急所データを登録しました')
        )
