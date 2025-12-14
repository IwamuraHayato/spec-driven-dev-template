# Claude Code Configuration

このファイルは **Claude Code** エディタでの開発をサポートするための設定ファイルです。

## 📖 概要

このテンプレートリポジトリは、仕様駆動開発のベストプラクティスを体系化したものです。Claude Code を使用する開発者向けに、以下の機能を提供します:

- **セキュリティ統合**: IPA「安全なウェブサイトの作り方」準拠のチェックリスト
- **開発規約**: Git ワークフロー、ブランチ戦略、コーディングスタイル
- **自動化**: GitHub Actions による CI/CD、PR 自動レビュー
- **テンプレート**: Next.js + FastAPI フルスタックアプリケーション
- **開発環境設定**: ESLint, Prettier, Ruff, mypy等の即座に使える設定ファイル（🆕 Phase 1完成）

## 🏗️ アーキテクチャ

### リポジトリ構造

```
spec-driven-dev-template/
├── .cursor/rules/              # Cursor エディタ用ルール（参考資料）
│   ├── security.mdc           # セキュリティ開発ルール
│   ├── branch_strategy.mdc    # ブランチ戦略
│   └── git_workflow.mdc       # Git 運用ルール
├── templates/                  # プロジェクトテンプレート
│   └── nextjs-fastapi/        # Next.js + FastAPI テンプレート
│       ├── .config-templates/ # 🆕 開発環境設定テンプレート
│       │   ├── frontend/      # Next.js設定（ESLint, Prettier, npm scripts）
│       │   └── backend/       # FastAPI設定（Ruff, mypy, pytest）
│       ├── .cursor/rules/     # 開発規約（9ファイル）
│       ├── .github/           # GitHub テンプレート
│       ├── .vscode/           # VS Code設定
│       └── docs/              # ドキュメント
├── generators/                 # 自動生成スクリプト
│   ├── interactive_setup.py   # 対話型セットアップ
│   └── setup.py               # 設定ファイルベース生成
├── USAGE.md                   # 使い方ガイド（開発環境セットアップ手順追加）
└── CLAUDE.md                  # 本ファイル（Claude Code 設定）
```

## 🔒 セキュリティ機能

### IPA セキュリティガイドライン準拠

このテンプレートは IPA「安全なウェブサイトの作り方」第11版に準拠したセキュリティチェック機能を統合しています。

#### セキュリティチェックリスト

詳細は以下のファイルを参照:

- **セキュリティ開発ルール**: [.cursor/rules/security.mdc](.cursor/rules/security.mdc)
  - セキュリティブランチでの開発フロー
  - Semgrep ルール実装ガイドライン
  - False Positive 対応戦略
  - セキュリティドキュメント整備基準

- **セキュリティチェックリスト**: [templates/nextjs-fastapi/docs/security-checklist.md](templates/nextjs-fastapi/docs/security-checklist.md)
  - フェーズ別チェック項目（設計・実装・テスト・運用）
  - 11 の基本対策（SQL インジェクション、XSS、CSRF など）
  - 14 の重要対策（アクセス制御、ログ管理など）

#### セキュリティ実装の基本原則

1. **Defense in Depth**: 多層防御を実装
2. **Test Before Deploy**: ローカルで必ず動作確認
3. **Document Everything**: セキュリティ実装は詳細にドキュメント化
4. **Review Required**: セキュリティ関連の変更は必ずレビュー

### 開発時の活用

Claude Code は以下のファイルを自動的に参照します:

- `.cursor/rules/security.mdc` - セキュリティ開発ルール
- `docs/security-checklist.md` - フェーズ別チェックリスト
- `docs/security/` - セキュリティリファレンス

**自動提案される機能**:
- ✅ セキュアなコードパターン
- ✅ 脆弱性対策のコード例
- ✅ IPA ガイドライン準拠チェック
- ✅ False Positive の識別支援

## 🎯 開発ワークフロー

### Git ブランチ戦略

詳細は [.cursor/rules/branch_strategy.mdc](.cursor/rules/branch_strategy.mdc) を参照。

**ブランチ構成**:
- `main` - 安定版（リリース可能な状態）
- `feature/*` - 新機能開発
- `fix/*` - バグ修正
- `docs/*` - ドキュメント更新
- `security/*` - セキュリティ関連実装
- `refactor/*` - リファクタリング

**基本フロー**:
```bash
# 1. 最新の main を取得
git checkout main
git pull origin main

# 2. ブランチ作成
git checkout -b feature/new-feature

# 3. 開発・コミット
git add .
git commit -m "feat: Add new feature"

# 4. プッシュして PR 作成
git push -u origin feature/new-feature
```

### セキュリティ実装フロー

詳細は [.cursor/rules/security.mdc](.cursor/rules/security.mdc) を参照。

```bash
# 1. セキュリティブランチ作成
git checkout -b security/implement-new-feature

# 2. 実装（セキュリティルール、テスト、ドキュメント）

# 3. ローカルでセキュリティチェック実行
./scripts/security/run-security-check.sh

# 4. テストプロジェクトで検証
cd /tmp/test-project
./scripts/security/run-security-check.sh

# 5. 問題がなければコミット
git add .
git commit -m "security: Implement new security feature with tests"

# 6. プッシュして PR 作成
git push -u origin security/implement-new-feature
```

## 📝 コーディング規約

### コミットメッセージ規約

詳細は [.cursor/rules/git_workflow.mdc](.cursor/rules/git_workflow.mdc) を参照。

**プレフィックス**:
- `feat:` - 新機能追加
- `fix:` - バグ修正
- `docs:` - ドキュメント変更のみ
- `security:` - セキュリティ関連の変更
- `refactor:` - リファクタリング
- `chore:` - ビルドプロセス、補助ツールの変更

**良い例**:
```bash
✅ feat: Add Django + React template support
✅ security: Implement IPA Phase 2 GitHub Actions workflow
✅ fix: Correct template variable replacement in generators
```

**悪い例**:
```bash
❌ update files
❌ fix bug
❌ add template and fix generator and update docs
```

## 🚀 使い方

### クイックスタート

1. **対話型セットアップ（推奨）**:
   ```bash
   cd generators/
   pip install -r requirements.txt
   python interactive_setup.py
   ```

2. **設定ファイルベース生成**:
   ```bash
   cd generators/
   python setup.py --config ../templates/nextjs-fastapi/template-config.yaml --output ../../my-new-project
   ```

詳細は [USAGE.md](USAGE.md) を参照してください。

## 🔗 関連ドキュメント

### テンプレートリポジトリ開発者向け

- [.cursor/rules/branch_strategy.mdc](.cursor/rules/branch_strategy.mdc) - ブランチ戦略
- [.cursor/rules/git_workflow.mdc](.cursor/rules/git_workflow.mdc) - Git 運用ルール
- [.cursor/rules/security.mdc](.cursor/rules/security.mdc) - セキュリティ開発ルール

### 生成されるプロジェクトの開発者向け

- [templates/nextjs-fastapi/CLAUDE.md.template](templates/nextjs-fastapi/CLAUDE.md.template) - AI 向け指示書サンプル
- [templates/nextjs-fastapi/docs/team-development-rules.md.template](templates/nextjs-fastapi/docs/team-development-rules.md.template) - チーム開発ルールサンプル
- [templates/nextjs-fastapi/docs/security-checklist.md](templates/nextjs-fastapi/docs/security-checklist.md) - セキュリティチェックリスト

### 使い方ガイド

- [USAGE.md](USAGE.md) - テンプレートの使い方
- [README.md](README.md) - プロジェクト概要

## 🤝 サポート

質問や問題がある場合:

1. [GitHub Issues](https://github.com/IwamuraHayato/spec-driven-dev-template/issues) で質問
2. [USAGE.md](USAGE.md) のトラブルシューティングを参照
3. セキュリティ関連は [.cursor/rules/security.mdc](.cursor/rules/security.mdc) を参照

## 🎨 Cursor エディタとの併用

このリポジトリには `.cursor/rules/` ディレクトリが含まれていますが、これは **Cursor エディタ専用** の機能です。

### エディタ別の対応

| エディタ | 主要設定ファイル | 補助資料 |
|---------|----------------|----------|
| **Cursor** | `.cursor/rules/*.mdc` | `CLAUDE.md` (本ファイル) |
| **Claude Code** | `CLAUDE.md` (本ファイル) | `.cursor/rules/*.mdc` (参考) |

**Claude Code ユーザーへの注意**:
- `.cursor/rules/` のファイルは直接読み込まれません
- 本ファイル (CLAUDE.md) が主要なルールソースです
- `.cursor/rules/` は参考資料として活用できます

## 📚 次のステップ

1. **テンプレート生成**: [USAGE.md](USAGE.md) の手順に従う
2. **セキュリティチェック**: [.cursor/rules/security.mdc](.cursor/rules/security.mdc) を確認
3. **開発開始**: Git ブランチを作成して開発スタート
