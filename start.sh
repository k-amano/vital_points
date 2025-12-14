#!/bin/bash

# 人体の急所学習アプリケーション - サーバー起動スクリプト

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# カラー出力
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}==================================================${NC}"
echo -e "${BLUE}  人体の急所学習アプリケーション - サーバー起動${NC}"
echo -e "${BLUE}==================================================${NC}"
echo ""

# PIDファイルのディレクトリを作成
mkdir -p .pids

# 既に起動しているかチェック
if [ -f .pids/backend.pid ] || [ -f .pids/frontend.pid ]; then
    echo -e "${YELLOW}警告: サーバーが既に起動している可能性があります${NC}"
    echo "終了する場合は ./stop.sh を実行してください"
    echo ""
    read -p "続行しますか？ (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "起動をキャンセルしました"
        exit 1
    fi
fi

# バックエンドサーバーの起動
echo -e "${GREEN}[1/2] Djangoバックエンドサーバーを起動中...${NC}"
cd backend
source ../venv/bin/activate

# ログディレクトリを作成
mkdir -p ../logs

# バックエンドをバックグラウンドで起動
nohup python manage.py runserver > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../.pids/backend.pid

echo "  → Django起動完了 (PID: $BACKEND_PID)"
echo "  → http://localhost:8000"
echo ""

# フロントエンドサーバーの起動
echo -e "${GREEN}[2/2] Reactフロントエンドサーバーを起動中...${NC}"
cd ../frontend

# フロントエンドをバックグラウンドで起動
nohup npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../.pids/frontend.pid

echo "  → React起動完了 (PID: $FRONTEND_PID)"
echo "  → http://localhost:5173"
echo ""

# 起動待機
echo -e "${BLUE}サーバーの起動を待機中...${NC}"
sleep 3

# サーバーの状態確認
echo ""
echo -e "${GREEN}✓ サーバー起動完了！${NC}"
echo ""
echo "==================================================="
echo "  アプリケーションURL:"
echo "  → http://localhost:5173"
echo ""
echo "  ログファイル:"
echo "  → logs/backend.log  (Djangoログ)"
echo "  → logs/frontend.log (Reactログ)"
echo ""
echo "  サーバーを終了するには:"
echo "  → ./stop.sh を実行"
echo "==================================================="
echo ""
echo -e "${YELLOW}ヒント: ログをリアルタイムで確認するには:${NC}"
echo "  tail -f logs/backend.log"
echo "  tail -f logs/frontend.log"
echo ""
