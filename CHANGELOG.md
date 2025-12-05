# Changelog

All notable changes to this template will be documented in this file.

## [1.1.0] - 2025-12-05

### Added - Phase 2: Automation Scripts

#### Generators (自動化スクリプト)
- ✅ **config_loader.py**: template-config.yaml パーサー
  - YAML 設定ファイルの読み込み
  - 変数の抽出と構造化
  - データベース固有設定のヘルパー関数

- ✅ **template_processor.py**: 変数置換エンジン
  - テキストファイルの変数置換 (`{{VARIABLE_NAME}}` 形式)
  - バイナリファイルの自動コピー
  - `.template` 拡張子の自動削除
  - 未置換変数の検出とレポート
  - 除外パターンによるファイルフィルタリング

- ✅ **validators.py**: 設定値バリデーター
  - 必須フィールドの存在確認
  - プロジェクト名の形式チェック（kebab-case推奨）
  - URL形式の検証
  - データベース設定の妥当性確認
  - ポート番号の範囲チェック
  - テストカバレッジ目標の妥当性検証
  - エラーと警告の分類表示

- ✅ **setup.py**: メイン生成スクリプト
  - CLI インターフェース（argparse）
  - 設定の読み込み → バリデーション → 処理 → 検証の完全フロー
  - `--config`, `--output`, `--template`, `--force`, `--no-validate` オプション
  - 処理結果サマリーと次のステップ表示

- ✅ **interactive_setup.py**: 対話型セットアップウィザード
  - ガイド付き質問形式でプロジェクト設定を収集
  - デフォルト値の提案と選択肢からの選択
  - 設定ファイルの自動生成（temp-config.yaml）
  - setup.py の自動呼び出し

- ✅ **requirements.txt**: Python 依存関係（PyYAML）
- ✅ **generators/README.md**: 生成スクリプトの詳細ドキュメント

#### Documentation Updates
- ✅ **USAGE.md**: 自動化スクリプトの使用方法を追加
  - 対話型セットアップ（推奨）
  - 設定ファイルを使用した生成
  - 手動セットアップ（上級者向け）に分類

- ✅ **MYSQL_SUPPORT.md**: MySQL 対応完了サマリー

### Improved

- **テンプレート生成の効率化**: 手動置換から自動生成へ（数秒でプロジェクト生成）
- **エラー検出の強化**: バリデーションにより設定ミスを事前検出
- **ユーザビリティ向上**: 対話型ウィザードで初心者でも簡単にセットアップ可能

---

## [1.0.0] - 2025-12-05

### Added - Phase 1: Template Extraction

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
