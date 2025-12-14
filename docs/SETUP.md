# セットアップガイド

## 必要な環境

### ソフトウェア要件

- Python 3.12以上
- Node.js 18.20.8以上（Vite 5を使用するため）
- Git
- pip3

### オペレーティングシステム

- Linux（WSL2含む）
- macOS
- Windows（WSL2推奨）

## 初期セットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd vital_points
```

### 2. Python仮想環境の作成

```bash
python3 -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

### 3. Pythonパッケージのインストール

```bash
pip install django djangorestframework django-cors-headers pillow
```

インストールされるパッケージ:
- Django 5.0
- djangorestframework
- django-cors-headers
- Pillow（画像処理）

### 4. データベースのマイグレーション

```bash
cd backend
python manage.py migrate
```

これにより`db.sqlite3`ファイルが作成され、必要なテーブルが作成されます。

### 5. 急所マスターデータの登録

```bash
python manage.py load_vital_points
```

出力例:
```
急所データを登録しました（新規: 70件, 更新: 0件）
```

### 6. Node.jsパッケージのインストール

```bash
cd ../frontend
npm install
```

インストールされる主要パッケージ:
- React 18.x
- Vite 5.4.21
- Axios

## 開発サーバーの起動

### スクリプトを使用した起動（推奨）

プロジェクトルートディレクトリで以下のスクリプトを実行:

#### サーバーの起動
```bash
./start.sh
```

このスクリプトは:
- Djangoバックエンドをバックグラウンドで起動
- Reactフロントエンドをバックグラウンドで起動
- PIDファイルを`.pids/`に保存
- ログを`logs/`に出力

#### サーバーの状態確認
```bash
./status.sh
```

現在のサーバー状態、PID、URL、最近のログを表示します。

#### サーバーの停止
```bash
./stop.sh
```

起動中のすべてのサーバープロセスを適切に終了します。

#### ログの確認

リアルタイムでログを確認:
```bash
# バックエンドログ
tail -f logs/backend.log

# フロントエンドログ
tail -f logs/frontend.log
```

### 手動での起動

#### バックエンド（Django）

ターミナル1:
```bash
cd backend
source ../venv/bin/activate
python manage.py runserver
```

サーバーが起動: `http://localhost:8000`

#### フロントエンド（React + Vite）

ターミナル2:
```bash
cd frontend
npm run dev
```

開発サーバーが起動: `http://localhost:5173`

### アプリケーションへのアクセス

ブラウザで `http://localhost:5173` を開く

## データ管理

### 急所データの更新

1. `vital_points_master.json`を編集
2. データを再読み込み:
```bash
cd backend
source ../venv/bin/activate
python manage.py load_vital_points
```

**重要**: `load_vital_points`コマンドは学習履歴を保持したままデータを更新します。

### データベースのリセット

完全にデータベースをリセットする場合:

```bash
cd backend
rm db.sqlite3
python manage.py migrate
python manage.py load_vital_points
```

**注意**: 学習履歴も削除されます。

### 学習履歴の確認

Djangoシェルを使用:

```bash
cd backend
python manage.py shell
```

シェル内で:
```python
from quiz.models import LearningHistory

# 全履歴を表示
for h in LearningHistory.objects.all():
    print(f"{h.vital_point.name}: 正解{h.correct_count}回, 不正解{h.incorrect_count}回")
```

## 画像の管理

### 画像の配置

急所の画像は以下のディレクトリに配置:
```
frontend/public/images/
```

画像ファイル名:
- `Scan2025-12-13_140703_000.png` - 頭部
- `Scan2025-12-13_140703_001.png` - 上肢
- `Scan2025-12-13_140703_002.png` - 胴部
- `Scan2025-12-13_140703_003.png` - 下肢前
- `Scan2025-12-13_140703_004.png` - 下肢後

### 画像の加工

元画像から正解部分をカットする場合:

```bash
python crop_images.py
```

設定は`crop_images.py`内の`crop_settings`で調整可能。

## トラブルシューティング

### Node.jsバージョンエラー

```
Error: You are using Node.js 18.20.8. Vite requires Node.js version 20.19+ or 22.12+
```

**解決方法**: Viteのバージョンを確認
- Vite 5.x: Node.js 18.x で動作
- Vite 7.x: Node.js 20.19+ が必要

package.jsonで確認:
```bash
cd frontend
cat package.json | grep vite
```

必要に応じてVite 5にダウングレード:
```bash
npm install vite@5.4.21 @vitejs/plugin-react@4.0.0
```

### CORS エラー

フロントエンドからAPIにアクセスできない場合:

1. `backend/backend/settings.py`を確認
2. `CORS_ALLOWED_ORIGINS`に使用しているオリジンが含まれているか確認:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]
```

### データベースロックエラー

複数のプロセスから同時にアクセスしている場合:
1. すべてのDjangoプロセスを停止
2. データベースファイルのロックを解除
3. 再起動

### 画像が表示されない

1. 画像ファイルが正しいディレクトリにあるか確認:
```bash
ls frontend/public/images/
```

2. ブラウザのコンソールでエラーを確認
3. 画像URLが正しいか確認（例: `http://localhost:5173/images/Scan2025-12-13_140703_000.png`）

## 開発ワークフロー

### コードの変更

1. フロントエンド:
   - `frontend/src/`内のファイルを編集
   - Viteがホットリロードで自動反映

2. バックエンド:
   - `backend/quiz/`内のファイルを編集
   - Djangoの開発サーバーが自動リロード

### マイグレーションの作成

モデルを変更した場合:

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 静的ファイルの収集（本番環境）

```bash
cd backend
python manage.py collectstatic
```

## 本番環境へのデプロイ

### フロントエンドのビルド

```bash
cd frontend
npm run build
```

`dist/`ディレクトリに本番用ファイルが生成されます。

### Django設定の変更

`backend/backend/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

# 静的ファイルの設定
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# CORS設定
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
]
```

### データベース

本番環境ではSQLiteではなくPostgreSQLやMySQLの使用を推奨。

## バックアップ

### データベースのバックアップ

```bash
cp backend/db.sqlite3 backend/db.sqlite3.backup
```

### データのエクスポート

```bash
cd backend
python manage.py dumpdata quiz > backup_data.json
```

### データのインポート

```bash
cd backend
python manage.py loaddata backup_data.json
```

## ログとデバッグ

### Djangoログの確認

開発サーバーのターミナル出力を確認

### フロントエンドのデバッグ

ブラウザの開発者ツール（F12）のConsoleタブを使用

### APIリクエストの確認

ブラウザの開発者ツールのNetworkタブでAPIリクエスト/レスポンスを確認

## ヘルプとサポート

### Django管理コマンド

```bash
python manage.py help
```

### 利用可能なカスタムコマンド

```bash
python manage.py help load_vital_points
```

### Djangoシェル

対話的にモデルやデータを操作:

```bash
python manage.py shell
```

例:
```python
from quiz.models import VitalPoint, LearningHistory, QuizSession
from django.utils import timezone

# 急所の一覧
VitalPoint.objects.all()

# 特定の急所を検索
VitalPoint.objects.filter(name='百会')

# 学習履歴の統計
total_correct = sum(h.correct_count for h in LearningHistory.objects.all())
total_incorrect = sum(h.incorrect_count for h in LearningHistory.objects.all())
print(f"正解: {total_correct}, 不正解: {total_incorrect}")
```

## まとめ

基本的なセットアップ手順:

1. Python仮想環境作成 → パッケージインストール
2. データベースマイグレーション → 急所データ登録
3. Node.jsパッケージインストール
4. バックエンド・フロントエンド両方のサーバー起動
5. `http://localhost:5173`にアクセス

質問や問題がある場合は、プロジェクトのIssueトラッカーを確認してください。
