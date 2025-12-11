# セキュリティテンプレート

このディレクトリには、すべてのプロジェクトテンプレートで共通使用されるセキュリティチェックファイルが含まれています。

## 概要

IPA「安全なウェブサイトの作り方 第7版」に準拠したセキュリティチェックシステムのテンプレートです。

## 技術スタック

### セキュリティ静的解析ツール

#### Bandit
- **目的**: Python専用のセキュリティ脆弱性検出
- **開発元**: PyCQA (Python Code Quality Authority)
- **主な機能**:
  - ASTベースのコード解析（抽象構文木）
  - 40種類以上の組み込みセキュリティチェック
  - 重大度（HIGH/MEDIUM/LOW）と信頼度による問題分類
  - SQLインジェクション、OSコマンドインジェクション、弱い暗号化などを検出
- **公式サイト**: https://bandit.readthedocs.io/

**検出例**:
```python
# B608: SQL injection (HIGH severity)
query = f"SELECT * FROM users WHERE id = {user_id}"

# B105: Hardcoded password (MEDIUM severity)
password = "admin123"

# B324: Weak hash algorithm (MEDIUM severity)
import hashlib
hashlib.md5(data)
```

#### Semgrep
- **目的**: 多言語対応の静的解析ツール（カスタムルール定義可能）
- **開発元**: r2c（Semgrep社）
- **対応言語**: Python, TypeScript, JavaScript, Go, Java, Ruby, PHPなど30言語以上
- **主な機能**:
  - YAMLベースのカスタムルール定義
  - パターンマッチングによる高精度検出
  - CWE（Common Weakness Enumeration）番号との紐付け
  - IPA「安全なウェブサイトの作り方」準拠のカスタムルール30個を実装
- **公式サイト**: https://semgrep.dev/

**検出例**:
```python
# ipa-sql-injection-string-format (ERROR severity)
query = "SELECT * FROM users WHERE name = '%s'" % user_input

# ipa-os-command-injection-shell-true (ERROR severity)
subprocess.run(f"ls {user_path}", shell=True)
```

```typescript
// ipa-xss-dangerously-set-inner-html (ERROR severity)
<div dangerouslySetInnerHTML={{__html: userInput}} />

// ipa-csrf-no-token-in-form (WARNING severity)
<form method="post" action="/delete">
  {/* CSRFトークンがない */}
</form>
```

### CI/CD自動化

#### GitHub Actions
- **目的**: プルリクエスト作成時の自動セキュリティチェック
- **ワークフロー**: `.github/workflows/security-check.yml`
- **主な機能**:
  - 並列ジョブ実行（Python/TypeScript同時チェック）
  - アーティファクト管理（JSON結果ファイルの保存・共有）
  - PRへの自動コメント投稿（GitHub API経由）
  - 重大な問題検出時のCI失敗

### カスタムルール実装

#### IPA準拠のSemgrepルール
- **Python用**: 16ルール（`scripts/security/semgrep-rules/ipa-python.yaml`）
- **TypeScript用**: 14ルール（`scripts/security/semgrep-rules/ipa-typescript.yaml`）
- **準拠基準**: IPA「安全なウェブサイトの作り方第7版」
- **メタデータ**:
  - IPA項目番号（例: `ipa_section: "1-(i)"`）
  - CWE番号（例: `cwe: "CWE-89"`）
  - OWASP分類（例: `owasp: "A03:2021"`）

### レポート生成

#### generate-pr-comment.py
- **言語**: Python 3.8+
- **機能**: JSON結果をMarkdownテーブルに変換
- **出力**: PRコメント用Markdown（重大度別色分け、IPA項目表示）

#### check-critical-issues.py
- **言語**: Python 3.8+
- **機能**: 重大な問題（HIGH/ERROR）のカウント
- **動作**: 重大な問題があればexit code 1でCIを失敗させる

### 実行環境要件

- **Python**: 3.8以上（Bandit, Semgrep, スクリプト実行用）
- **Bash**: 4.0以上（`run-security-check.sh`実行用）
- **Git**: 2.0以上（GitHub Actions連携用）
- **GitHub Actions**: ubuntu-latest（CI/CD環境）

## ディレクトリ構成

```
.security-template/
├── README.md                           # このファイル
├── .bandit                             # Bandit設定（Python）
├── .github/
│   └── workflows/
│       └── security-check.yml         # GitHub Actionsワークフロー
└── scripts/
    └── security/
        ├── semgrep-rules/
        │   ├── ipa-python.yaml        # Python用IPAルール
        │   └── ipa-typescript.yaml    # TypeScript用IPAルール
        ├── run-security-check.sh      # ローカル実行スクリプト
        ├── generate-pr-comment.py     # PRコメント生成
        └── check-critical-issues.py   # 重大問題チェック
```

## 使用方法

### 新規プロジェクト生成時

`generators/interactive_setup.py` が自動的に以下を実行します：

1. このテンプレートから生成先プロジェクトにファイルをコピー
2. テンプレート固有の `.security-config.yaml` でカスタマイズ
3. 不要なルールを除外

### 手動セットアップ

既存プロジェクトに手動で追加する場合：

```bash
# プロジェクトルートで実行
cp -r .security-template/.bandit .
cp -r .security-template/.github .
cp -r .security-template/scripts .

# テンプレート固有の設定があれば適用
# 例: templates/nextjs-fastapi/.security-config.yaml
```

## テンプレート別カスタマイズ

各テンプレートは `.security-config.yaml` でカスタマイズ可能：

```yaml
# templates/nextjs-fastapi/.security-config.yaml
security:
  languages:
    - python
    - typescript

  bandit:
    enabled: true
    exclude_dirs:
      - backend/migrations
      - backend/tests

  semgrep:
    python:
      enabled: true
      rules:
        - ipa-sql-injection
        - ipa-os-command-injection
        # ... 有効化するルール

    typescript:
      enabled: true
      rules:
        - ipa-xss-dangerously-set-inner-html
        - ipa-xss-dangerous-url-scheme
        # ... 有効化するルール
```

## セキュリティチェックの動作フロー

### ローカル実行の流れ

開発者がローカルで `./scripts/security/run-security-check.sh` を実行すると、以下の流れでセキュリティチェックが行われます：

```
開発者
  │
  ▼
./scripts/security/run-security-check.sh 実行
  │
  ├─ 1. Bandit実行（Python）
  │    ├─ プロジェクト全体をスキャン
  │    ├─ .bandit の設定に基づいて除外ディレクトリをスキップ
  │    └─ bandit-results.json に結果を出力
  │
  ├─ 2. Semgrep実行（Python）
  │    ├─ scripts/security/semgrep-rules/ipa-python.yaml のルール適用
  │    ├─ プロジェクト全体をスキャン
  │    └─ semgrep-python-results.json に結果を出力
  │
  └─ 3. Semgrep実行（TypeScript）
       ├─ scripts/security/semgrep-rules/ipa-typescript.yaml のルール適用
       ├─ プロジェクト全体をスキャン
       └─ semgrep-typescript-results.json に結果を出力
  │
  ▼
ターミナルに結果表示（カラー出力）
  ├─ ✅ 問題なし
  ├─ ⚠️  警告あり
  └─ ❌ 重大な問題検出
```

### GitHub Actions CI/CDの流れ

PRが作成されると、自動的にGitHub Actionsが起動します：

```
Pull Request作成（main/develop向け）
  │
  ▼
.github/workflows/security-check.yml 実行
  │
  ├─── Job 1: python-security（並列実行）
  │      ├─ Bandit実行
  │      └─ Semgrep（Python）実行
  │
  ├─── Job 2: typescript-security（並列実行）
  │      └─ Semgrep（TypeScript）実行
  │
  ▼
両Jobの完了を待つ
  │
  ▼
Job 3: security-report
  ├─ 1. 各Jobのアーティファクトをダウンロード
  │      ├─ bandit-results.json
  │      ├─ semgrep-python-results.json
  │      └─ semgrep-typescript-results.json
  │
  ├─ 2. scripts/security/generate-pr-comment.py 実行
  │      ├─ 各JSONファイルを解析
  │      ├─ Markdownテーブル形式に変換
  │      └─ pr-comment.md を生成
  │
  ├─ 3. PRにコメントを自動投稿（GitHub API経由）
  │      ├─ セキュリティ問題の一覧表示
  │      ├─ 重大度別に色分け（🔴 HIGH, 🟡 MEDIUM, 🟢 LOW）
  │      └─ IPA項目番号とCWE番号も表示
  │
  └─ 4. scripts/security/check-critical-issues.py 実行
         ├─ 重大な問題（HIGH/ERROR）の数をカウント
         └─ 重大な問題があればCIを失敗させる（exit 1）
```

### スキャン対象範囲

#### 対象ファイル

セキュリティチェックは以下のファイルを対象にします：

**Bandit（Python）**:
- 拡張子: `.py`
- 対象: プロジェクト全体の再帰的スキャン
- 実行コマンド例: `bandit -r . -c .bandit`

**Semgrep（Python）**:
- 拡張子: `.py`
- 対象: プロジェクト全体の再帰的スキャン
- 実行コマンド例: `semgrep --config scripts/security/semgrep-rules/ipa-python.yaml .`

**Semgrep（TypeScript/JavaScript）**:
- 拡張子: `.ts`, `.tsx`, `.js`, `.jsx`
- 対象: プロジェクト全体の再帰的スキャン
- 実行コマンド例: `semgrep --config scripts/security/semgrep-rules/ipa-typescript.yaml .`

#### 除外ディレクトリ・ファイル

以下は自動的に除外されます：

**Bandit（.bandit で設定）**:
```ini
exclude_dirs = [
  '/tests',           # テストコード
  '/test',            # テストコード
  '/.venv',           # Python仮想環境
  '/venv',            # Python仮想環境
  '/node_modules',    # Node.js依存関係
  '/.git'             # Gitメタデータ
]
```

**Semgrep（.semgrepignore で設定可能）**:
```
# .semgrepignore ファイルを作成して除外パターンを追加
tests/
**/*_test.py
**/*.test.ts
node_modules/
.venv/
```

#### スキャン範囲のカスタマイズ

**特定ディレクトリのみをチェック**:
```bash
# Pythonバックエンドのみ
bandit -r ./backend -c .bandit
semgrep --config scripts/security/semgrep-rules/ipa-python.yaml ./backend

# TypeScriptフロントエンドのみ
semgrep --config scripts/security/semgrep-rules/ipa-typescript.yaml ./frontend
```

**コード内で特定行を除外**:
```python
# Banditの除外
# nosec B608
query = f"SELECT * FROM users WHERE id = {user_id}"
```

```typescript
// Semgrepの除外
// nosemgrep: ipa-xss-dangerously-set-inner-html
<div dangerouslySetInnerHTML={{__html: trustedContent}} />
```

## 検出可能な脆弱性

| IPA項目 | 脆弱性 | Python | TypeScript |
|---------|--------|:------:|:----------:|
| 1-(i) | SQLインジェクション | ✅ | - |
| 2-(i) | OSコマンドインジェクション | ✅ | - |
| 3-(i) | ディレクトリトラバーサル | ✅ | - |
| 4-(i)(iii) | セッション管理の不備 | ✅ | - |
| 5-(i)(ii)(iii) | XSS | ✅ | ✅ |
| 6-(i) | CSRF | - | ✅ |
| 7-(i) | HTTPヘッダインジェクション | ✅ | - |
| 8-(i) | メールヘッダインジェクション | ✅ | - |
| その他 | 機密情報・暗号化 | ✅ | ✅ |

## メンテナンス

### ルールの追加

新しいセキュリティルールを追加する場合：

1. `scripts/security/semgrep-rules/ipa-python.yaml` または `ipa-typescript.yaml` を編集
2. ルールにIPAセクション番号をメタデータとして追加
3. テストして動作確認

### ツールのバージョン更新

GitHub Actionsワークフローで使用するツールのバージョンを更新：

```yaml
# .github/workflows/security-check.yml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'  # ← バージョン更新
```

## 関連ドキュメント

- [セキュリティ実装ガイド](../docs/security/README.md)
- [セキュリティ規約](../templates/nextjs-fastapi/.cursor/rules/security.mdc)
- [セキュリティチェックリスト](../templates/nextjs-fastapi/docs/security-checklist.md)
- [IPA 安全なウェブサイトの作り方](https://www.ipa.go.jp/security/vuln/websecurity/)
