#!/usr/bin/env python3
"""
画像の表から正確に急所データを抽出するスクリプト
画像の表を左→中央→右の順に、上から下へ読む
"""

import json

# 画像1: 頭部・頸部・顔面の急所（25個）
# 表を注意深く左列→中央列→右列の順に読む
vital_points_data = {
    "Scan2025-12-13_140703_000.png": {
        "category": "頭部・頸部・顔面の急所",
        "points": [
            # 左列
            {"number": "①", "name": "百会", "reading": "ひゃくえ"},
            {"number": "②", "name": "顎会", "reading": "しんえ"},
            {"number": "③", "name": "耳門", "reading": "じもん"},
            {"number": "④", "name": "顎", "reading": "さんかく"},
            {"number": "⑤", "name": "人迎", "reading": "じんげい"},
            {"number": "⑥", "name": "水突", "reading": "しょうしょつ"},
            {"number": "⑦", "name": "気舎", "reading": "きしゃ"},
            {"number": "⑧", "name": "缺盆", "reading": "けつぼん"},
            # 中央列
            {"number": "⑨", "name": "四合", "reading": "よんごう"},
            {"number": "⑩", "name": "三合", "reading": "さんごう"},
            {"number": "⑪", "name": "三月", "reading": "みつき"},
            {"number": "⑫", "name": "風府", "reading": "ふうふ"},
            {"number": "⑬", "name": "瘂門", "reading": "あもん"},
            {"number": "⑭", "name": "脳戸", "reading": "のうこ"},
            {"number": "⑮", "name": "哮戸", "reading": "あもん"},
            {"number": "⑯", "name": "瘂門", "reading": "あもん"},
            # 右列
            {"number": "⑰", "name": "天柱", "reading": "てんちゅう"},
            {"number": "⑱", "name": "巓谷", "reading": "いんこく"},
            {"number": "⑲", "name": "顋脈", "reading": "けつみゃく"},
            {"number": "⑳", "name": "風府", "reading": "ふうふ"},
            {"number": "㉑", "name": "胸鎖", "reading": "けいさ"},
            {"number": "㉒", "name": "竜尾", "reading": "まのつぼ"},
        ]
    }
}

# まず画像1だけ作成して確認してもらう
def save_to_json():
    """データをJSONファイルに保存"""
    with open('vital_points_master_correct.json', 'w', encoding='utf-8') as f:
        json.dump(vital_points_data, f, ensure_ascii=False, indent=2)
    print("急所データを vital_points_master_correct.json に保存しました")

    for image_name, data in vital_points_data.items():
        count = len(data['points'])
        print(f"{image_name}: {count}箇所")
        print("番号と名前:")
        for point in data['points']:
            print(f"  {point['number']} {point['name']} ({point['reading']})")

if __name__ == "__main__":
    save_to_json()
