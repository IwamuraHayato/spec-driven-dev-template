# Changelog

All notable changes to this template will be documented in this file.

## [1.0.0] - 2025-12-05

### Added

#### Core Templates
- ✅ **CLAUDE.md.template**: AI 向けプロジェクト指示書
  - プロジェクト概要、技術スタック、アーキテクチャ説明
  - コーディングパターン（Server/Client Component、API Client、FastAPI サービス）
  - よく使うコマンド、トラブルシューティング

- ✅ **README.md.template**: プロジェクト README
  - セットアップ手順、技術スタック、主要機能
  - よく使うコマンド、開発規約、テスト、API ドキュメント

- ✅ **template-config.yaml**: 変数定義ファイル
  - プロジェクト情報、技術スタック、チーム情報、開発設定

#### .cursor/rules/ (開発規約)
- ✅ **code_style.mdc**: コーディングスタイル規約
  - Next.js/TypeScript: PascalCase/camelCase/kebab-case
  - Python/FastAPI: snake_case/PascalCase、型ヒント必須

- ✅ **commit_message.mdc**: コミットメッセージ規約
  - type(scope): subject フォーマット
  - タイプ一覧、スコープ例、実装例

- ✅ **branch_strategy.mdc**: ブランチ戦略
  - main/develop/feature/bugfix/refactor/hotfix
  - ブランチ命名規則、マージルール、ブランチ保護

- ✅ **testing.mdc**: テスト規約
  - Frontend: Jest + React Testing Library
  - Backend: pytest + pytest-asyncio
  - カバレッジ目標 80%以上

- ✅ **security.mdc**: セキュリティ規約
  - 認証・認可、環境変数管理、データベースセキュリティ
  - API セキュリティ、フロントエンドセキュリティ

- ✅ **documentation.mdc**: ドキュメント作成規約
  - ドキュメントの種類、コメント規約、更新タイミング

- ✅ **github.mdc**: GitHub 操作ルール
  - Issue 管理、PR 管理、GitHub Actions、GitHub CLI 活用

- ✅ **pull_request_summary.mdc**: PR 要約ルール
  - PR タイトル、説明の構造、レビュアーへの配慮

#### .github/ (GitHub テンプレート)
- ✅ **ISSUE_TEMPLATE/product-backlog.md**: Product Backlog テンプレート
  - 何をやるのか、なぜやるのか、技術的制約、受入条件、タスク

- ✅ **ISSUE_TEMPLATE/bug-report.md**: Bug Report テンプレート
  - バグの概要、再現手順、期待/実際の動作、環境情報

- ✅ **PULL_REQUEST_TEMPLATE/pull_request_template.md**: PR テンプレート
  - 概要、関連タスク、やったこと/やらないこと、影響範囲、テスト

- ✅ **workflows/claude-pr-review.yml**: Claude 自動レビュー
  - PR 作成・更新時に Claude がコードレビュー
  - 重複レビュー防止、コミットハッシュ追跡

- ✅ **workflows/pr-checks.yml**: PR チェック
  - Frontend: Type check、Lint、Format、Test、Build
  - Backend: Ruff lint/format、MyPy、pytest、Coverage

#### .vscode/ (VS Code 設定)
- ✅ **settings.json**: エディタ設定
  - 保存時自動フォーマット、言語別フォーマッター設定
  - Python: Ruff、TypeScript: Prettier

- ✅ **extensions.json**: 推奨拡張機能
  - Prettier、ESLint、Ruff、Python、Tailwind CSS、Copilot 等

#### docs/ (ドキュメント)
- ✅ **dev/REVIEW.md**: コードレビューガイドライン
  - 8つのレビューポイント（スタイル、設計、動作、パフォーマンス、セキュリティ等）
  - Next.js 特有、FastAPI 特有のチェックポイント

- ✅ **team-development-rules.md.template**: チーム開発ルール
  - プロジェクト管理、ドキュメント管理、開発環境、コミュニケーション
  - セキュリティ、品質保証、リリース管理、緊急時対応

#### ルートドキュメント
- ✅ **README.md**: テンプレートリポジトリの README
- ✅ **USAGE.md**: テンプレート使用ガイド
- ✅ **CHANGELOG.md**: 変更履歴

### Technical Stack

- **Frontend**: Next.js 15+, TypeScript, Tailwind CSS, Zustand
- **Backend**: Python 3.12+, FastAPI, PostgreSQL 14+ または MySQL 8.0+, SQLAlchemy, Alembic
- **Development**: Docker, GitHub Actions, VS Code, Ruff, ESLint, Prettier
- **Database Flexibility**: PostgreSQL および MySQL の両方に対応。変数置換システムにより簡単に切り替え可能

### References

このテンプレートは以下のプロジェクトから抽出されたベストプラクティスに基づいています:
- **mandom-tech0_healthcare**: 男性向けヘルスケアサービス（Flutter + FastAPI）

## [Unreleased]

### Planned Features

- 🔜 **自動置換スクリプト**: `generators/setup.sh` による変数自動置換
- 🔜 **CLAUDE.md ジェネレーター**: 対話形式での CLAUDE.md 生成
- 🔜 **技術スタック別バリエーション**:
  - Next.js + NestJS
  - React + Express
  - Vue + Laravel
- 🔜 **ドメイン固有テンプレート**:
  - ヘルスケア向け（HIPAA 準拠）
  - EC サイト向け（PCI-DSS 準拠）
  - SaaS 向け（マルチテナント対応）
