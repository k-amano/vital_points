#!/bin/bash

# 人体の急所学習アプリケーション - サーバー状態確認スクリプト

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}==================================================${NC}"
echo -e "${BLUE}  人体の急所学習アプリケーション - サーバー状態${NC}"
echo -e "${BLUE}==================================================${NC}"
echo ""

RUNNING=0

# バックエンドサーバーの状態確認
echo -e "${BLUE}[Django バックエンド]${NC}"
if [ -f .pids/backend.pid ]; then
    BACKEND_PID=$(cat .pids/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo -e "  状態: ${GREEN}起動中${NC}"
        echo "  PID: $BACKEND_PID"
        echo "  URL: http://localhost:8000"
        echo "  ログ: logs/backend.log"
        RUNNING=$((RUNNING + 1))
    else
        echo -e "  状態: ${RED}停止中${NC} (PIDファイルが残っています)"
        echo "  → ./stop.sh を実行してクリーンアップしてください"
    fi
else
    echo -e "  状態: ${RED}停止中${NC}"
fi

echo ""

# フロントエンドサーバーの状態確認
echo -e "${BLUE}[React フロントエンド]${NC}"
if [ -f .pids/frontend.pid ]; then
    FRONTEND_PID=$(cat .pids/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo -e "  状態: ${GREEN}起動中${NC}"
        echo "  PID: $FRONTEND_PID"
        echo "  URL: http://localhost:5173"
        echo "  ログ: logs/frontend.log"
        RUNNING=$((RUNNING + 1))
    else
        echo -e "  状態: ${RED}停止中${NC} (PIDファイルが残っています)"
        echo "  → ./stop.sh を実行してクリーンアップしてください"
    fi
else
    echo -e "  状態: ${RED}停止中${NC}"
fi

echo ""
echo "==================================================="

if [ $RUNNING -eq 2 ]; then
    echo -e "${GREEN}✓ 両方のサーバーが起動中です${NC}"
    echo ""
    echo "アプリケーションにアクセス:"
    echo "  → http://localhost:5173"
elif [ $RUNNING -eq 1 ]; then
    echo -e "${YELLOW}⚠ 一部のサーバーのみ起動しています${NC}"
    echo ""
    echo "両方を起動するには:"
    echo "  → ./stop.sh && ./start.sh"
else
    echo -e "${RED}✗ サーバーは起動していません${NC}"
    echo ""
    echo "起動するには:"
    echo "  → ./start.sh"
fi

echo "==================================================="
echo ""

# ログファイルの確認
if [ -f logs/backend.log ] || [ -f logs/frontend.log ]; then
    echo -e "${BLUE}最近のログ情報:${NC}"
    echo ""

    if [ -f logs/backend.log ]; then
        echo -e "${YELLOW}Backend (最終5行):${NC}"
        tail -5 logs/backend.log | sed 's/^/  /'
        echo ""
    fi

    if [ -f logs/frontend.log ]; then
        echo -e "${YELLOW}Frontend (最終5行):${NC}"
        tail -5 logs/frontend.log | sed 's/^/  /'
        echo ""
    fi
fi
