#!/usr/bin/env python3
"""
画像から急所データを抽出するスクリプト
画像を確認しながら手動でデータを作成します
"""

import json

# 画像を目視で確認して作成した急所データ
vital_points_data = {
    "Scan2025-12-13_140703_000.png": {
        "category": "頭部・頸部・顔面の急所",
        "count": 25,
        "points": [
            {"number": "①", "name": "百会", "reading": "ひゃくえ"},
            {"number": "②", "name": "四合", "reading": "しごう"},
            {"number": "③", "name": "天柱", "reading": "てんちゅう"},
            {"number": "④", "name": "顋会", "reading": "しんえ"},
            {"number": "⑤", "name": "三合", "reading": "さんごう"},
            {"number": "⑥", "name": "巓谷", "reading": "いんこく"},
            {"number": "⑦", "name": "耳門", "reading": "じもん"},
            {"number": "⑧", "name": "蝶谷", "reading": "ちょうこく"},
            {"number": "⑨", "name": "顋脈", "reading": "けいみゃく"},
            {"number": "⑩", "name": "人迎", "reading": "じんげい"},
            {"number": "⑪", "name": "風府", "reading": "ふうふ"},
            {"number": "⑫", "name": "胸鎖", "reading": "きょうさ"},
            {"number": "⑬", "name": "闕門", "reading": "けつもん"},
            {"number": "⑭", "name": "竜尾", "reading": "りゅうび"},
            {"number": "⑮", "name": "顋月", "reading": "あごつき"},
            {"number": "⑯", "name": "脳戸", "reading": "のうこ"},
            {"number": "⑰", "name": "嗇囲", "reading": "まのつぼ"},
            {"number": "⑱", "name": "唖門", "reading": "あもん"},
            {"number": "⑲", "name": "哮音", "reading": "けいおん"},
            {"number": "⑳", "name": "顋中", "reading": "けいちゅう"},
            {"number": "㉑", "name": "顋扶", "reading": "けいふ"},
            {"number": "㉒", "name": "気舎", "reading": "きしゃ"},
            {"number": "㉓", "name": "缺盆", "reading": "けつぼん"},
            {"number": "㉔", "name": "天窓", "reading": "てんそう"},
            {"number": "㉕", "name": "天容", "reading": "てんよう"},
        ]
    },
    "Scan2025-12-13_140703_001.png": {
        "category": "上肢（手足）の急所",
        "count": 15,
        "points": [
            # 内側
            {"number": "①", "name": "肩髃", "reading": "けんぐう"},
            {"number": "②", "name": "少海", "reading": "しょうかい"},
            {"number": "③", "name": "尺沢", "reading": "しゃくたく"},
            {"number": "④", "name": "経渠", "reading": "けいきょ"},
            {"number": "⑤", "name": "太淵", "reading": "たいえん"},
            {"number": "⑥", "name": "心包", "reading": "しんぽう"},
            {"number": "⑦", "name": "指谷", "reading": "しこく"},
            # 外側
            {"number": "①", "name": "巨骨", "reading": "ここつ"},
            {"number": "②", "name": "肘髎", "reading": "ちゅうりょう"},
            {"number": "③", "name": "天井", "reading": "てんせい"},
            {"number": "④", "name": "曲池", "reading": "きょくち"},
            {"number": "⑤", "name": "頭谷", "reading": "ずこく"},
            {"number": "⑥", "name": "谷谷", "reading": "こくこく"},
            {"number": "⑦", "name": "中渚", "reading": "ちゅうしょ"},
            {"number": "⑧", "name": "甲谷", "reading": "こうこく"},
        ]
    },
    "Scan2025-12-13_140703_002.png": {
        "category": "胴部の急所",
        "count": 11,
        "points": [
            {"number": "①", "name": "天突", "reading": "てんとつ"},
            {"number": "②", "name": "気舎", "reading": "きしゃ"},
            {"number": "③", "name": "三鎖", "reading": "さんさ"},
            {"number": "④", "name": "巨闕", "reading": "だんちゅう"},
            {"number": "⑤", "name": "金的", "reading": "きんてき"},
            {"number": "⑥", "name": "上脘", "reading": "じょうかん"},
            {"number": "⑦", "name": "膺宮", "reading": "ようきゅう"},
            {"number": "⑧", "name": "鷺尾", "reading": "けいび"},
            {"number": "⑨", "name": "建里", "reading": "けんり"},
            {"number": "⑩", "name": "水月", "reading": "すいげつ"},
            {"number": "⑪", "name": "膺陵", "reading": "ようりょう"},
        ]
    },
    "Scan2025-12-13_140703_003.png": {
        "category": "急所名（漢字・よみがな）",
        "count": 12,
        "points": [
            {"number": "①", "name": "気衝", "reading": "きしょう"},
            {"number": "②", "name": "夜光", "reading": "やこう"},
            {"number": "③", "name": "伏兎", "reading": "ふくと"},
            {"number": "④", "name": "風市", "reading": "ふうし"},
            {"number": "⑤", "name": "血海", "reading": "けっかい"},
            {"number": "⑥", "name": "梁丘", "reading": "りょうきゅう"},
            {"number": "⑦", "name": "膝眼", "reading": "しつがん"},
            {"number": "⑧", "name": "三里", "reading": "さんり"},
            {"number": "⑨", "name": "甲利", "reading": "こうり"},
            {"number": "⑩", "name": "三陰交", "reading": "さんいんこう"},
            {"number": "⑪", "name": "太衝", "reading": "たいしょう"},
            {"number": "⑫", "name": "陥谷", "reading": "かんこく"},
        ]
    },
    "Scan2025-12-13_140703_004.png": {
        "category": "急所名（漢字・よみがな）",
        "count": 9,
        "points": [
            {"number": "⑬", "name": "承扶", "reading": "しょうふ"},
            {"number": "⑭", "name": "殷門", "reading": "いんもん"},
            {"number": "⑮", "name": "委中", "reading": "いちゅう"},
            {"number": "⑯", "name": "委陽", "reading": "いよう"},
            {"number": "⑰", "name": "陰谷", "reading": "いんこく"},
            {"number": "⑱", "name": "承筋", "reading": "しょうきん"},
            {"number": "⑲", "name": "築賓", "reading": "ちくひん"},
            {"number": "⑳", "name": "外踝", "reading": "がいか"},
            {"number": "㉑", "name": "内踝", "reading": "ないか"},
        ]
    }
}

def save_to_json():
    """データをJSONファイルに保存"""
    with open('vital_points_master.json', 'w', encoding='utf-8') as f:
        json.dump(vital_points_data, f, ensure_ascii=False, indent=2)
    print("急所データを vital_points_master.json に保存しました")

def print_summary():
    """データのサマリーを表示"""
    total = 0
    for image_name, data in vital_points_data.items():
        count = len(data['points'])
        total += count
        print(f"{image_name}: {count}箇所")
    print(f"\n合計: {total}箇所")

if __name__ == "__main__":
    save_to_json()
    print_summary()
