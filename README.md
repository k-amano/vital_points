# 人体の急所学習アプリケーション

人体の急所70箇所の名前を覚えるための学習アプリケーションです。画像を使った4択クイズ形式で効率的に学習できます。

## 特徴

- 画像ベースの4択クイズ形式
- ふりがな付きで学習しやすい
- 学習履歴の永続的な保存
- 苦手な問題を優先的に出題する機能
- リアルタイムで更新される統計情報

## スクリーンショット

### スタート画面
学習状況の統計が表示され、通常モードまたは苦手な問題モードを選択できます。

### クイズ画面
問題文、選択肢（ふりがな付き）、急所の画像が表示されます。

### 統計画面
各急所ごとの学習履歴と正解率を確認できます。

## 技術スタック

### フロントエンド
- React.js 18.x
- Vite 5.4.21
- Axios

### バックエンド
- Django 5.0
- Django REST Framework
- SQLite 3

## クイックスタート

### 1. 環境構築

```bash
# Python仮想環境の作成
python3 -m venv venv
source venv/bin/activate

# Pythonパッケージのインストール
pip install django djangorestframework django-cors-headers pillow

# データベースのセットアップ
cd backend
python manage.py migrate
python manage.py load_vital_points

# Node.jsパッケージのインストール
cd ../frontend
npm install
```

### 2. サーバーの起動

ターミナル1（バックエンド）:
```bash
cd backend
source ../venv/bin/activate
python manage.py runserver
```

ターミナル2（フロントエンド）:
```bash
cd frontend
npm run dev
```

### 3. アクセス

ブラウザで `http://localhost:5173` を開く

## ドキュメント

詳細なドキュメントは`docs/`フォルダを参照してください:

- [SPECIFICATION.md](docs/SPECIFICATION.md) - アプリケーション仕様書
- [API.md](docs/API.md) - API仕様書
- [SETUP.md](docs/SETUP.md) - セットアップガイド

## データ構成

- **画像1（頭部）**: 22箇所
- **画像2（上肢）**: 15箇所
- **画像3（胴部）**: 12箇所
- **画像4（下肢前）**: 12箇所
- **画像5（下肢後）**: 9箇所

**合計**: 70箇所の急所

## 主要機能

### 通常モード
全70箇所の急所をランダムな順序で出題します。

### 苦手な問題モード
不正解が多い急所を優先的に出題し、効率的に弱点を克服できます。

### 学習履歴
- 各急所ごとの正解・不正解回数を記録
- 正解率を自動計算
- データベースに永続的に保存

### 統計情報
- 累計正解数・不正解数
- 全体の正解率
- 急所別の詳細統計

## プロジェクト構造

```
vital_points/
├── backend/           # Djangoバックエンド
│   ├── quiz/          # メインアプリケーション
│   └── db.sqlite3     # データベース
├── frontend/          # Reactフロントエンド
│   ├── src/           # ソースコード
│   └── public/        # 静的ファイル（画像など）
├── docs/              # ドキュメント
├── venv/              # Python仮想環境
└── README.md          # このファイル
```

## 開発

### データの更新

急所データを更新する場合:

1. `vital_points_master.json`を編集
2. データを再読み込み:
```bash
cd backend
python manage.py load_vital_points
```

学習履歴は保持されます。

### マイグレーション

モデルを変更した場合:

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

## ライセンス

このプロジェクトは教育目的で作成されています。

## バージョン

- v1.0.0 (2025-12-14): 初回リリース

## サポート

問題や質問がある場合は、プロジェクトのIssueトラッカーをご利用ください。
