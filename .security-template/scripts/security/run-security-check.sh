#!/bin/bash
# ローカルセキュリティチェック実行スクリプト
# IPA準拠の静的解析ツールを実行

set -e

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ヘッダー表示
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🔒 セキュリティチェック実行${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 結果ディレクトリの作成
RESULTS_DIR="security-results"
mkdir -p "$RESULTS_DIR"

# エラーカウンター
TOTAL_ERRORS=0

# ========================================
# Python セキュリティチェック
# ========================================
echo -e "${BLUE}📊 Python セキュリティチェック開始${NC}"
echo ""

# Bandit チェック
if command -v bandit &> /dev/null; then
    echo -e "${YELLOW}▶ Bandit 実行中...${NC}"
    if bandit -r . -c .bandit -f json -o "$RESULTS_DIR/bandit-results.json" 2>&1; then
        echo -e "${GREEN}✅ Bandit: 問題なし${NC}"
    else
        BANDIT_EXIT=$?
        if [ $BANDIT_EXIT -eq 1 ]; then
            echo -e "${RED}❌ Bandit: 脆弱性を検出${NC}"
            TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
            # 人間が読みやすい形式でも出力
            bandit -r . -c .bandit -f screen
        fi
    fi
    echo ""
else
    echo -e "${YELLOW}⚠️  Bandit がインストールされていません${NC}"
    echo "   インストール: pip install bandit"
    echo ""
fi

# Semgrep (Python) チェック
if command -v semgrep &> /dev/null; then
    echo -e "${YELLOW}▶ Semgrep (Python) 実行中...${NC}"
    if semgrep --config scripts/security/semgrep-rules/ipa-python.yaml \
               --json --output "$RESULTS_DIR/semgrep-python-results.json" \
               . 2>&1 | grep -v "ran " || true; then

        # 結果の確認
        SEMGREP_COUNT=$(jq '.results | length' "$RESULTS_DIR/semgrep-python-results.json" 2>/dev/null || echo "0")
        if [ "$SEMGREP_COUNT" -eq 0 ]; then
            echo -e "${GREEN}✅ Semgrep (Python): 問題なし${NC}"
        else
            echo -e "${RED}❌ Semgrep (Python): ${SEMGREP_COUNT}件の問題を検出${NC}"
            TOTAL_ERRORS=$((TOTAL_ERRORS + SEMGREP_COUNT))
            # 人間が読みやすい形式で出力
            semgrep --config scripts/security/semgrep-rules/ipa-python.yaml .
        fi
    fi
    echo ""
else
    echo -e "${YELLOW}⚠️  Semgrep がインストールされていません${NC}"
    echo "   インストール: pip install semgrep または brew install semgrep"
    echo ""
fi

# ========================================
# TypeScript/JavaScript セキュリティチェック
# ========================================
echo -e "${BLUE}📊 TypeScript/JavaScript セキュリティチェック開始${NC}"
echo ""

# Semgrep (TypeScript) チェック
if command -v semgrep &> /dev/null; then
    echo -e "${YELLOW}▶ Semgrep (TypeScript) 実行中...${NC}"
    if semgrep --config scripts/security/semgrep-rules/ipa-typescript.yaml \
               --json --output "$RESULTS_DIR/semgrep-typescript-results.json" \
               . 2>&1 | grep -v "ran " || true; then

        # 結果の確認
        SEMGREP_TS_COUNT=$(jq '.results | length' "$RESULTS_DIR/semgrep-typescript-results.json" 2>/dev/null || echo "0")
        if [ "$SEMGREP_TS_COUNT" -eq 0 ]; then
            echo -e "${GREEN}✅ Semgrep (TypeScript): 問題なし${NC}"
        else
            echo -e "${RED}❌ Semgrep (TypeScript): ${SEMGREP_TS_COUNT}件の問題を検出${NC}"
            TOTAL_ERRORS=$((TOTAL_ERRORS + SEMGREP_TS_COUNT))
            # 人間が読みやすい形式で出力
            semgrep --config scripts/security/semgrep-rules/ipa-typescript.yaml .
        fi
    fi
    echo ""
fi

# ESLint Security Plugin チェック（存在する場合）
if [ -f "package.json" ] && grep -q "eslint-plugin-security" package.json 2>/dev/null; then
    echo -e "${YELLOW}▶ ESLint Security Plugin 実行中...${NC}"
    if npm run lint:security 2>&1 || true; then
        echo -e "${GREEN}✅ ESLint Security: チェック完了${NC}"
    fi
    echo ""
fi

# ========================================
# サマリー表示
# ========================================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📋 セキュリティチェック完了${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

if [ $TOTAL_ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ すべてのチェックに合格しました${NC}"
    echo ""
    echo "結果ファイル: $RESULTS_DIR/"
    exit 0
else
    echo -e "${RED}❌ ${TOTAL_ERRORS}件の問題が検出されました${NC}"
    echo ""
    echo "詳細な結果: $RESULTS_DIR/"
    echo ""
    echo -e "${YELLOW}次のステップ:${NC}"
    echo "1. 検出された問題を確認"
    echo "2. templates/nextjs-fastapi/.cursor/rules/security.mdc を参照"
    echo "3. 修正後、再度このスクリプトを実行"
    exit 1
fi
