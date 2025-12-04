# 仕様駆動開発テンプレート - プロジェクトサマリー

## 📊 完成したファイル一覧

### ルートディレクトリ (4ファイル)
- ✅ README.md - テンプレートリポジトリの概要
- ✅ USAGE.md - テンプレート使用ガイド
- ✅ CHANGELOG.md - 変更履歴
- ✅ .gitignore - Git 除外設定

### templates/nextjs-fastapi/ (20ファイル)

#### AI向け指示書 (2ファイル)
- ✅ CLAUDE.md.template - Claude Code 用プロジェクト指示書（15,000+ 文字）
- ✅ README.md.template - プロジェクト README テンプレート

#### 開発規約 .cursor/rules/ (8ファイル)
- ✅ code_style.mdc - コーディングスタイル
- ✅ commit_message.mdc - コミットメッセージ規約
- ✅ branch_strategy.mdc - ブランチ戦略
- ✅ testing.mdc - テスト規約
- ✅ security.mdc - セキュリティ規約
- ✅ documentation.mdc - ドキュメント作成規約
- ✅ github.mdc - GitHub 操作ルール
- ✅ pull_request_summary.mdc - PR 要約ルール

#### GitHub テンプレート .github/ (5ファイル)
- ✅ ISSUE_TEMPLATE/product-backlog.md - Product Backlog
- ✅ ISSUE_TEMPLATE/bug-report.md - Bug Report
- ✅ PULL_REQUEST_TEMPLATE/pull_request_template.md - PR テンプレート
- ✅ workflows/claude-pr-review.yml - Claude 自動レビュー
- ✅ workflows/pr-checks.yml - PR チェック (Frontend + Backend)

#### VS Code 設定 .vscode/ (2ファイル)
- ✅ settings.json - エディタ設定
- ✅ extensions.json - 推奨拡張機能

#### ドキュメント docs/ (2ファイル)
- ✅ dev/REVIEW.md - コードレビューガイドライン
- ✅ team-development-rules.md.template - チーム開発ルール

#### 設定ファイル (1ファイル)
- ✅ template-config.yaml - 変数定義

## 📈 統計情報

- **総ファイル数**: 24ファイル
- **総文字数**: 約50,000文字
- **カバーする領域**: 
  - AI指示書
  - 開発規約（8種類）
  - GitHub運用（Issue/PR/CI/CD）
  - エディタ設定
  - ドキュメント
  - チーム開発ルール

## 🎯 実装した7つの仕組み

1. ✅ **AI向け指示書** (CLAUDE.md.template)
2. ✅ **.cursor/rules/** (8つの開発規約)
3. ✅ **GitHub Issueテンプレート** (2種類)
4. ✅ **PRテンプレート** (1種類)
5. ✅ **チーム開発ルール** (team-development-rules.md.template)
6. ✅ **GitHub Actions** (2種類)
7. ✅ **VS Code設定** (settings.json + extensions.json)

## 📦 変数置換システム

### 置換が必要な変数 (11個)

1. `{{PROJECT_NAME}}` - プロジェクト名
2. `{{PROJECT_DESCRIPTION}}` - プロジェクト説明
3. `{{REPOSITORY_URL}}` - リポジトリURL
4. `{{INFRASTRUCTURE_PLATFORM}}` - インフラ (AWS/GCP/Azure)
5. `{{ORGANIZATION_NAME}}` - 組織名
6. `{{PM_NAME}}` - PM名
7. `{{TECH_LEAD_NAME}}` - 技術リード名
8. `{{TARGET_USER_DESCRIPTION}}` - ターゲットユーザー説明
9. `{{TEST_COVERAGE_TARGET}}` - テストカバレッジ目標
10. `{{LICENSE}}` - ライセンス
11. `{{FEATURES_LIST}}` - 機能リスト

### 置換対象ファイル (5ファイル)

1. CLAUDE.md.template
2. README.md.template
3. docs/team-development-rules.md.template
4. docs/dev/REVIEW.md
5. .github/workflows/claude-pr-review.yml

## 🚀 使用方法

### クイックスタート (3ステップ)

```bash
# 1. テンプレートをコピー
cp -r spec-driven-dev-template/templates/nextjs-fastapi/* /path/to/new-project/

# 2. 変数を置換
# VS Codeで一括置換: Cmd/Ctrl + Shift + H

# 3. .template拡張子を削除
mv CLAUDE.md.template CLAUDE.md
mv README.md.template README.md
mv docs/team-development-rules.md.template docs/team-development-rules.md
```

詳細は [USAGE.md](USAGE.md) を参照

## 🎨 技術スタック

### Frontend
- Next.js 15+ (App Router)
- TypeScript
- Tailwind CSS
- Zustand (状態管理)

### Backend
- Python 3.12+
- FastAPI
- PostgreSQL 14+
- SQLAlchemy (ORM)
- Alembic (マイグレーション)

### Development
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- VS Code
- Ruff (Python linter/formatter)
- ESLint + Prettier (JS/TS)

## 📝 次のステップ

### Phase 2: 自動化スクリプト開発 (予定)

```bash
# 対話形式での変数入力とテンプレート適用
./generators/setup.sh

# 出力例
✓ プロジェクト名を入力: my-awesome-app
✓ プロジェクト説明を入力: 次世代Webアプリ
✓ インフラを選択 (AWS/GCP/Azure): AWS
...
✅ テンプレート適用完了！
```

### Phase 3: 技術スタック別バリエーション (予定)

```
templates/
├── nextjs-fastapi/      # ✅ 完成
├── nextjs-nestjs/       # 🔜 計画中
├── react-express/       # 🔜 計画中
└── vue-laravel/         # 🔜 計画中
```

## 🎉 Phase 1 完了

Next.js + FastAPI プロジェクト向けの完全な仕様駆動開発テンプレートが完成しました。

すぐに新規プロジェクトに適用可能です！
