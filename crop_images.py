#!/usr/bin/env python3
"""
画像の正解表示部分をカットするスクリプト
"""

from PIL import Image
import os

# 画像ディレクトリ
input_dir = 'backend/static/images'
output_dir = 'backend/static/images'

# 各画像に対するクロップ設定
# (top_ratio, right_ratio, bottom_ratio, left_ratio)
# 残す範囲の比率を指定: 1.0 = 100%残す、0.5 = 50%残す
crop_settings = {
    'Scan2025-12-13_140703_000.png': {
        'top': 1.0,    # 上部100%残す
        'bottom': 0.5, # 下部は50%の位置まで（50%カット）
        'left': 1.0,   # 左側100%残す
        'right': 1.0,  # 右側100%残す
    },
    'Scan2025-12-13_140703_001.png': {
        'top': 1.0,
        'bottom': 0.45,
        'left': 1.0,
        'right': 1.0,
    },
    'Scan2025-12-13_140703_002.png': {
        'top': 1.0,
        'bottom': 0.45,
        'left': 1.0,
        'right': 1.0,
    },
    'Scan2025-12-13_140703_003.png': {
        'top': 1.0,
        'bottom': 1.0,   # 下部はカットしない
        'left': 1.0,
        'right': 0.55,   # 右側55%の位置まで（45%カット）
    },
    'Scan2025-12-13_140703_004.png': {
        'top': 1.0,
        'bottom': 1.0,
        'left': 1.0,
        'right': 0.55,
    },
}

def crop_image(image_path, settings):
    """画像を指定された設定でクロップ"""
    # 画像を開く
    img = Image.open(image_path)
    width, height = img.size

    # クロップする範囲を計算
    left = 0
    top = 0
    right = int(width * settings['right'])
    bottom = int(height * settings['bottom'])

    # クロップ実行
    cropped = img.crop((left, top, right, bottom))

    return cropped

def main():
    print("画像のクロップ処理を開始します...")

    for filename, settings in crop_settings.items():
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # オリジナルから復元
        backup_path = input_path.replace('.png', '_original.png')

        if os.path.exists(backup_path):
            # バックアップから読み込む
            source_path = backup_path
            print(f"📦 バックアップから復元: {filename}")
        else:
            # 初回実行の場合、現在の画像をバックアップ
            source_path = input_path
            img = Image.open(input_path)
            img.save(backup_path)
            print(f"📦 バックアップ作成: {backup_path}")

        # クロップ処理
        cropped_img = crop_image(source_path, settings)
        cropped_img.save(output_path)

        # カット情報を表示
        info_parts = []
        if settings['bottom'] < 1.0:
            info_parts.append(f"下部{int((1-settings['bottom'])*100)}%カット")
        if settings['right'] < 1.0:
            info_parts.append(f"右側{int((1-settings['right'])*100)}%カット")

        info = ", ".join(info_parts) if info_parts else "カットなし"
        print(f"✅ {filename} - {info}")

    print("\n処理が完了しました！")
    print("元の画像は *_original.png として保存されています。")

if __name__ == "__main__":
    main()
