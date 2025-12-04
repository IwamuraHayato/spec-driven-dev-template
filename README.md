# 仕様駆動開発テンプレート (Spec-Driven Development Template)

Next.js + FastAPI プロジェクト向けの包括的な開発テンプレートリポジトリです。AI 向け指示書、開発規約、GitHub テンプレート、VS Code 設定など、仕様駆動開発に必要なすべてを含んでいます。

## 📦 含まれるもの

### 1. AI 向け指示書
- **CLAUDE.md**: Claude Code 用のプロジェクト指示書（アーキテクチャ、コーディングパターン、コマンド集）
- プロジェクト概要から実装パターンまで完全に文書化

### 2. .cursor/rules/ (開発規約)
- `code_style.mdc`: コーディングスタイル規約
- `commit_message.mdc`: コミットメッセージ規約
- `branch_strategy.mdc`: ブランチ戦略
- `testing.mdc`: テスト規約
- `security.mdc`: セキュリティ規約
- `documentation.mdc`: ドキュメント作成規約
- `github.mdc`: GitHub 操作ルール
- `pull_request_summary.mdc`: PR 要約ルール

### 3. GitHub テンプレート
- **Issue テンプレート**: Product Backlog, Bug Report
- **PR テンプレート**: 変更内容・影響範囲・テストを明記
- **GitHub Actions**: Claude 自動レビュー、PR チェック

### 4. VS Code 設定
- `.vscode/settings.json`: 統一された開発環境設定
- `.vscode/extensions.json`: 推奨拡張機能リスト

### 5. ドキュメント
- `docs/dev/REVIEW.md`: コードレビューガイドライン
- `docs/team-development-rules.md`: チーム開発ルール

### 6. 設定ファイル
- `template-config.yaml`: プロジェクト変数定義

## 🚀 使い方

### ステップ 1: テンプレートをコピー

```bash
# テンプレートリポジトリをクローン
git clone https://github.com/your-org/spec-driven-dev-template.git

# プロジェクトディレクトリにコピー
cp -r spec-driven-dev-template/templates/nextjs-fastapi/* /path/to/your-project/
```

### ステップ 2: 変数を置換

`template-config.yaml` を参考に、以下の変数をプロジェクト固有の値に置換してください:

```yaml
project:
  name: "MyAwesomeApp"
  description: "次世代 Web アプリケーション"
  repository_url: "https://github.com/your-org/my-awesome-app"

team:
  organization: "Your Organization"
  pm_name: "山田太郎"
  tech_lead: "鈴木花子"

features:
  - "ユーザー認証機能"
  - "データダッシュボード"
  - "レポート生成機能"
```

置換が必要な変数:
- `{{PROJECT_NAME}}`
- `{{PROJECT_DESCRIPTION}}`
- `{{REPOSITORY_URL}}`
- `{{INFRASTRUCTURE_PLATFORM}}` (AWS / GCP / Azure)
- `{{DATABASE_TYPE}}` (PostgreSQL / MySQL)
- `{{DATABASE_VERSION}}` (PostgreSQL 14+ / MySQL 8.0+)
- `{{DATABASE_PORT}}` (PostgreSQL: 5432 / MySQL: 3306)
- `{{DATABASE_CLIENT_TOOLS}}` (データベースクライアントツール)
- `{{DATABASE_URL_EXAMPLE}}` (データベース接続 URL 例)
- `{{ORGANIZATION_NAME}}`
- `{{PM_NAME}}`
- `{{TECH_LEAD_NAME}}`
- `{{FEATURES_LIST}}`
- `{{TARGET_USER_DESCRIPTION}}`
- `{{TEST_COVERAGE_TARGET}}` (通常 80)
- `{{LICENSE}}` (MIT / Apache 2.0 / Proprietary)

### ステップ 3: 置換スクリプトを実行（準備中）

```bash
# 自動置換スクリプト（今後実装予定）
./generators/setup.sh --config template-config.yaml
```

### ステップ 4: プロジェクト固有のカスタマイズ

- CLAUDE.md: プロジェクト固有の情報を追加
- docs/team-development-rules.md: チーム固有のルールを追加
- .github/workflows/: CI/CD パイプラインをカスタマイズ

## 📋 テンプレートの構造

```
spec-driven-dev-template/
├── templates/
│   └── nextjs-fastapi/           # Next.js + FastAPI テンプレート
│       ├── .cursor/
│       │   └── rules/            # 開発規約（8ファイル）
│       ├── .github/
│       │   ├── ISSUE_TEMPLATE/   # Issue テンプレート
│       │   ├── PULL_REQUEST_TEMPLATE/
│       │   └── workflows/        # GitHub Actions
│       ├── .vscode/
│       │   ├── settings.json     # VS Code 設定
│       │   └── extensions.json   # 推奨拡張機能
│       ├── docs/
│       │   ├── dev/
│       │   │   └── REVIEW.md     # レビューガイドライン
│       │   └── team-development-rules.md.template
│       ├── CLAUDE.md.template    # AI 向け指示書
│       ├── README.md.template    # プロジェクト README
│       └── template-config.yaml  # 変数定義
└── generators/                   # 自動生成スクリプト（今後実装）
```

## 🎯 このテンプレートが解決する問題

### Before (テンプレートなし)

- ❌ 各プロジェクトでゼロから設定ファイルを作成
- ❌ コーディングスタイルがバラバラ
- ❌ コミットメッセージが統一されていない
- ❌ レビュー基準が曖昧
- ❌ AI が適切にコードを生成できない

### After (テンプレートあり)

- ✅ 数分でプロジェクトセットアップ完了
- ✅ 統一されたコーディングスタイル
- ✅ 明確なコミットメッセージ規約
- ✅ 体系化されたレビュープロセス
- ✅ AI が規約に従ったコードを自動生成

## 🔧 カスタマイズ例

### 別の技術スタックに対応

現在は Next.js + FastAPI のみですが、以下のように拡張可能:

```
templates/
├── nextjs-fastapi/      # ✅ 実装済み
├── nextjs-nestjs/       # 🔜 今後実装
├── react-express/       # 🔜 今後実装
└── vue-laravel/         # 🔜 今後実装
```

### ドメイン固有のルール追加

例: ヘルスケアプロジェクト向け

```yaml
# template-config.yaml に追加
domain_specific:
  compliance: ["HIPAA", "GDPR"]
  security_requirements:
    - "医療データの暗号化"
    - "アクセスログの記録"
```

## 📚 参考プロジェクト

このテンプレートは、以下のプロジェクトから抽出されたベストプラクティスを基にしています:

- **mandom-tech0_healthcare**: 男性向けヘルスケアサービス（Flutter + FastAPI）

## 🤝 貢献

テンプレートの改善提案を歓迎します！

1. このリポジトリをフォーク
2. 改善ブランチを作成 (`git checkout -b improvement/amazing-improvement`)
3. 変更をコミット (`git commit -m 'docs: improve template documentation'`)
4. ブランチにプッシュ (`git push origin improvement/amazing-improvement`)
5. プルリクエストを作成

## 📝 ライセンス

MIT License

## 🔗 関連リンク

- [Next.js 公式ドキュメント](https://nextjs.org/docs)
- [FastAPI 公式ドキュメント](https://fastapi.tiangolo.com/)
- [Claude Code](https://claude.ai/code)
- [Cursor](https://cursor.sh/)

## 📧 お問い合わせ

質問や提案がある場合は、Issue を作成してください。
