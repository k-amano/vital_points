#!/usr/bin/env python3
"""
編集したテキストファイルから急所データを生成するスクリプト
"""

import json
import re

def parse_edit_file(filepath):
    """編集ファイルを解析してデータ構造を作成"""

    vital_points_data = {}
    current_image = None
    current_category = None
    current_section = None  # 内側/外側の区別用

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        # コメント行をスキップ
        if not line or line.startswith('#'):
            # 画像情報を抽出
            if '画像' in line and '.png' in line:
                match = re.search(r'(Scan.*\.png)', line)
                if match:
                    current_image = match.group(1)
                    vital_points_data[current_image] = {
                        'category': '',
                        'points': []
                    }
                # カテゴリを抽出
                if '頭部' in line:
                    current_category = '頭部・頸部・顔面の急所'
                elif '上肢' in line:
                    current_category = '上肢（手足）の急所'
                elif '胴部' in line:
                    current_category = '胴部の急所'
                elif '下肢' in line and '前面' in line:
                    current_category = '下肢の急所（前面）'
                elif '下肢' in line and '後面' in line:
                    current_category = '下肢の急所（後面）'

                if current_image and current_category:
                    vital_points_data[current_image]['category'] = current_category

            # セクション情報
            if '[内側]' in line:
                current_section = '内側'
            elif '[外側]' in line:
                current_section = '外側'
            continue

        # データ行を解析
        if current_image and ',' in line:
            parts = line.split(',')
            if len(parts) >= 3:
                number = parts[0].strip()
                name = parts[1].strip()
                reading = parts[2].strip()

                # 空欄をスキップ
                if name and reading:
                    vital_points_data[current_image]['points'].append({
                        'number': number,
                        'name': name,
                        'reading': reading
                    })

    return vital_points_data

def save_to_json(data, output_file):
    """JSONファイルに保存"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def print_summary(data):
    """サマリーを表示"""
    total = 0
    print("\n=== 急所データサマリー ===")
    for image_name, image_data in data.items():
        count = len(image_data['points'])
        total += count
        print(f"\n{image_name}:")
        print(f"  カテゴリ: {image_data['category']}")
        print(f"  件数: {count}箇所")
        print(f"  番号範囲: {image_data['points'][0]['number']} ～ {image_data['points'][-1]['number']}")

        # 最初の3件を表示
        print("  データ例:")
        for point in image_data['points'][:3]:
            print(f"    {point['number']} {point['name']} ({point['reading']})")

    print(f"\n合計: {total}箇所")
    return total

def main():
    input_file = 'vital_points_edit.txt'
    output_file = 'vital_points_master.json'

    print(f"編集ファイルを読み込んでいます: {input_file}")

    try:
        data = parse_edit_file(input_file)

        if not data:
            print("エラー: データが見つかりませんでした")
            return

        # サマリー表示
        total = print_summary(data)

        # JSONに保存
        save_to_json(data, output_file)
        print(f"\n✅ {output_file} に保存しました")

        # データベースに登録するか確認
        print("\nデータベースに登録するには以下を実行してください:")
        print("  cd backend")
        print("  source ../venv/bin/activate")
        print("  python manage.py load_vital_points")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
