#!/bin/bash

# 人体の急所学習アプリケーション - サーバー終了スクリプト

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}==================================================${NC}"
echo -e "${BLUE}  人体の急所学習アプリケーション - サーバー終了${NC}"
echo -e "${BLUE}==================================================${NC}"
echo ""

# PIDファイルの存在確認
if [ ! -f .pids/backend.pid ] && [ ! -f .pids/frontend.pid ]; then
    echo -e "${YELLOW}サーバーは起動していません${NC}"
    echo ""
    exit 0
fi

STOPPED=0

# バックエンドサーバーの終了
if [ -f .pids/backend.pid ]; then
    BACKEND_PID=$(cat .pids/backend.pid)
    echo -e "${GREEN}[1/2] Djangoバックエンドサーバーを終了中...${NC}"

    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        kill $BACKEND_PID 2>/dev/null

        # プロセスが終了するまで待機（最大5秒）
        for i in {1..10}; do
            if ! ps -p $BACKEND_PID > /dev/null 2>&1; then
                break
            fi
            sleep 0.5
        done

        # まだ動いている場合は強制終了
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            echo -e "${YELLOW}  → 強制終了中...${NC}"
            kill -9 $BACKEND_PID 2>/dev/null
        fi

        echo "  → Django終了完了 (PID: $BACKEND_PID)"
        STOPPED=$((STOPPED + 1))
    else
        echo -e "${YELLOW}  → プロセスが見つかりません (PID: $BACKEND_PID)${NC}"
    fi

    rm -f .pids/backend.pid
else
    echo -e "${YELLOW}[1/2] Djangoバックエンドは起動していません${NC}"
fi

echo ""

# フロントエンドサーバーの終了
if [ -f .pids/frontend.pid ]; then
    FRONTEND_PID=$(cat .pids/frontend.pid)
    echo -e "${GREEN}[2/2] Reactフロントエンドサーバーを終了中...${NC}"

    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        # npm run devの子プロセスも含めて終了
        pkill -P $FRONTEND_PID 2>/dev/null
        kill $FRONTEND_PID 2>/dev/null

        # プロセスが終了するまで待機（最大5秒）
        for i in {1..10}; do
            if ! ps -p $FRONTEND_PID > /dev/null 2>&1; then
                break
            fi
            sleep 0.5
        done

        # まだ動いている場合は強制終了
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            echo -e "${YELLOW}  → 強制終了中...${NC}"
            pkill -9 -P $FRONTEND_PID 2>/dev/null
            kill -9 $FRONTEND_PID 2>/dev/null
        fi

        echo "  → React終了完了 (PID: $FRONTEND_PID)"
        STOPPED=$((STOPPED + 1))
    else
        echo -e "${YELLOW}  → プロセスが見つかりません (PID: $FRONTEND_PID)${NC}"
    fi

    rm -f .pids/frontend.pid
else
    echo -e "${YELLOW}[2/2] Reactフロントエンドは起動していません${NC}"
fi

echo ""

# Viteの子プロセスも確実に終了
echo -e "${BLUE}関連プロセスのクリーンアップ中...${NC}"
pkill -f "vite" 2>/dev/null
pkill -f "manage.py runserver" 2>/dev/null

echo ""
if [ $STOPPED -gt 0 ]; then
    echo -e "${GREEN}✓ サーバー終了完了！${NC}"
else
    echo -e "${YELLOW}サーバーは既に停止していました${NC}"
fi
echo ""
