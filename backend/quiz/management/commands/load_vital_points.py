import json
from django.core.management.base import BaseCommand
from quiz.models import VitalPoint


class Command(BaseCommand):
    help = '急所マスターデータをJSONから読み込む'

    def handle(self, *args, **options):
        json_path = '/home/administrator/Projects/vital_points/vital_points_master.json'

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 学習履歴を保持するため、削除せずに更新または作成を行う
        updated_count = 0
        created_count = 0

        for image_name, image_data in data.items():
            category = image_data['category']
            for point in image_data['points']:
                # image_file、number、nameの組み合わせで既存データを検索
                vital_point, created = VitalPoint.objects.update_or_create(
                    image_file=image_name,
                    number=point['number'],
                    name=point['name'],
                    defaults={
                        'reading': point['reading'],
                        'category': category,
                    }
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'急所データを登録しました（新規: {created_count}件, 更新: {updated_count}件）'
            )
        )
