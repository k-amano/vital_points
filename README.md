# 人体の急所 学習アプリ

人体の急所72箇所を学習するためのWebアプリケーションです。

## 機能

- ランダム順での急所の出題（4択形式）
- 正解/不正解の即時フィードバック
- 不正解の場合は同じ問題を再出題
- 学習履歴の記録（正解数、不正解数）
- 学習統計の表示
- セッションの中断・再開機能

## 技術スタック

- **フロントエンド**: React.js + Vite
- **バックエンド**: Django + Django REST Framework
- **データベース**: SQLite

## セットアップ手順

### 1. 仮想環境の有効化

```bash
source venv/bin/activate
```

### 2. バックエンドの起動

```bash
cd backend
python manage.py runserver
```

Djangoサーバーが http://localhost:8000 で起動します。

### 3. フロントエンドの起動（別のターミナルで）

```bash
cd frontend
npm run dev
```

Reactアプリが http://localhost:5173 で起動します。

### 4. ブラウザでアクセス

http://localhost:5173 をブラウザで開いてアプリを使用できます。

## データについて

- 急所データ: 72箇所の急所情報（名前、読み仮名、画像）
- 画像ファイル: `backend/static/images/` に5つのPNG画像を配置

## APIエンドポイント

### 急所マスターデータ
- `GET /api/vital-points/` - 全急所の取得

### 学習履歴
- `GET /api/learning-history/` - 学習履歴の取得
- `GET /api/learning-history/statistics/` - 統計情報の取得
- `GET /api/learning-history/weak_points/` - 苦手な急所の取得

### クイズセッション
- `POST /api/quiz-sessions/start_new_session/` - 新規セッション開始
- `GET /api/quiz-sessions/{id}/current_question/` - 現在の問題取得
- `POST /api/quiz-sessions/{id}/submit_answer/` - 回答送信
- `POST /api/quiz-sessions/{id}/pause/` - セッション中断
- `POST /api/quiz-sessions/{id}/resume/` - セッション再開
- `POST /api/quiz-sessions/{id}/complete/` - セッション完了

## 使い方

1. **開始画面**
   - 「新しいセッションを開始」をクリックして学習を開始
   - 「詳細な統計を見る」で学習履歴を確認

2. **学習画面**
   - 急所の画像と番号が表示されます
   - 4つの選択肢から正解を選択
   - 正解すると次の問題へ進む
   - 不正解の場合は正解が表示され、もう一度同じ問題に挑戦

3. **統計画面**
   - 累計の正解数、不正解数、正解率を確認
   - 苦手な急所（不正解が多い順）を表示
   - 全履歴の詳細を確認

## 開発者向け

### データの再読み込み

```bash
cd backend
python manage.py load_vital_points
```

### 管理画面

http://localhost:8000/admin でDjango管理画面にアクセスできます。

スーパーユーザーを作成:
```bash
python manage.py createsuperuser
```

## ライセンス

This project is for educational purposes.
