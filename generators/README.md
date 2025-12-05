# Template Generators

自動化スクリプトで、テンプレートから新規プロジェクトを数秒で生成できます。

## セットアップ

```bash
cd generators/

# 依存関係のインストール
pip install -r requirements.txt
```

## 使い方

### 方法 1: 対話型セットアップ（推奨）

対話形式で質問に答えていくだけでプロジェクトを生成:

```bash
python interactive_setup.py
```

**実行例**:
```
🚀 Spec-Driven Development Template - Interactive Setup
======================================================================

📋 Project Information
----------------------------------------------------------------------
Project name (lowercase, use hyphens) [my-awesome-project]: my-healthcare-app
Project description [A modern web application]: Healthcare診断プラットフォーム
...

🎉 Project generated successfully!
```

### 方法 2: 設定ファイルを使用

`template-config.yaml` を編集してから実行:

```bash
# 基本的な使用方法
python setup.py --config ../templates/nextjs-fastapi/template-config.yaml --output ../../my-new-project

# 既存ディレクトリを上書き
python setup.py --config config.yaml --output ../my-project --force

# バリデーションをスキップ（非推奨）
python setup.py --config config.yaml --output ../my-project --no-validate
```

## スクリプト一覧

### `interactive_setup.py`

**対話型セットアップウィザード**

- ✅ ガイド付きの質問形式
- ✅ デフォルト値の提案
- ✅ 選択肢からの選択
- ✅ 設定ファイルの自動生成

**使用例**:
```bash
python interactive_setup.py
```

---

### `setup.py`

**メインの生成スクリプト**

設定ファイルを読み込み、テンプレートから新規プロジェクトを生成します。

**引数**:
- `--config`: template-config.yaml へのパス（必須）
- `--output`: 出力ディレクトリ（必須）
- `--template`: 使用するテンプレート名（デフォルト: nextjs-fastapi）
- `--force`: 既存ディレクトリを上書き
- `--no-validate`: バリデーションをスキップ

**使用例**:
```bash
python setup.py --config config.yaml --output ../my-project
```

---

### `config_loader.py`

**設定ファイルローダー**

`template-config.yaml` を読み込み、変数を抽出します。

**使用例**:
```bash
python config_loader.py ../templates/nextjs-fastapi/template-config.yaml
```

**出力**:
```
=== Configuration Variables ===
PROJECT_NAME: my-awesome-project
PROJECT_DESCRIPTION: A modern web application
...

=== Database Configuration ===
type: PostgreSQL
port: 5432
driver: asyncpg
...
```

---

### `template_processor.py`

**テンプレート処理エンジン**

テンプレートファイルの変数を置換し、新規プロジェクトを生成します。

**使用例**:
```bash
python template_processor.py templates/nextjs-fastapi output '{"PROJECT_NAME":"test"}'
```

**機能**:
- ✅ テキストファイルの変数置換（`{{VARIABLE_NAME}}` 形式）
- ✅ バイナリファイルのコピー
- ✅ `.template` 拡張子の自動削除
- ✅ 未置換変数の検出

---

### `validators.py`

**設定値バリデーター**

設定値の妥当性をチェックし、エラーや警告を表示します。

**使用例**:
```bash
python validators.py '{"PROJECT_NAME":"my-app","DATABASE_TYPE":"PostgreSQL"}'
```

**検証項目**:
- ✅ 必須フィールドの存在確認
- ✅ プロジェクト名の形式チェック
- ✅ URL形式の検証
- ✅ データベース設定の妥当性
- ✅ ポート番号の範囲チェック
- ✅ テストカバレッジ目標の妥当性

---

## 変数リスト

テンプレートで使用可能な変数:

| 変数名 | 説明 | 例 |
|--------|------|-----|
| `{{PROJECT_NAME}}` | プロジェクト名 | `my-healthcare-app` |
| `{{PROJECT_DESCRIPTION}}` | プロジェクト説明 | `Healthcare診断プラットフォーム` |
| `{{REPOSITORY_URL}}` | リポジトリURL | `https://github.com/org/repo` |
| `{{DATABASE_TYPE}}` | データベースの種類 | `PostgreSQL` / `MySQL` |
| `{{DATABASE_VERSION}}` | データベースバージョン | `14+` / `8.0+` |
| `{{DATABASE_PORT}}` | データベースポート | `5432` / `3306` |
| `{{DATABASE_CLIENT_TOOLS}}` | クライアントツール | `psql, pgAdmin, DBeaver` |
| `{{DATABASE_URL_EXAMPLE}}` | 接続URL例 | `postgresql+asyncpg://...` |
| `{{INFRASTRUCTURE_PLATFORM}}` | インフラプラットフォーム | `AWS` / `GCP` / `Azure` |
| `{{ORGANIZATION_NAME}}` | 組織名 | `Your Company` |
| `{{PM_NAME}}` | プロジェクトマネージャー名 | `山田太郎` |
| `{{TECH_LEAD_NAME}}` | 技術リード名 | `鈴木花子` |
| `{{TARGET_USER_DESCRIPTION}}` | ターゲットユーザー説明 | `エンドユーザー向け...` |
| `{{TEST_COVERAGE_TARGET}}` | テストカバレッジ目標 | `80` |
| `{{LICENSE}}` | ライセンス | `MIT` / `Apache 2.0` |
| `{{FEATURES_LIST}}` | 主要機能リスト | `- 機能1\n- 機能2` |

## トラブルシューティング

### ImportError: No module named 'yaml'

```bash
pip install -r requirements.txt
```

### Template not found

テンプレートディレクトリが存在することを確認:

```bash
ls -la ../templates/nextjs-fastapi/
```

### Output directory already exists

`--force` フラグを使用して上書き:

```bash
python setup.py --config config.yaml --output ../my-project --force
```

### Unreplaced variables in output

一部の変数が置換されていない場合、`template-config.yaml` に値を追加してください。

## 開発

### テスト

各スクリプトは単独でテスト可能:

```bash
# config_loader のテスト
python config_loader.py ../templates/nextjs-fastapi/template-config.yaml

# validator のテスト
python validators.py '{"PROJECT_NAME":"test-app","DATABASE_TYPE":"PostgreSQL"}'

# template_processor のテスト
python template_processor.py ../templates/nextjs-fastapi /tmp/test-output '{"PROJECT_NAME":"test"}'
```

### デバッグ

Python の `-v` フラグで詳細ログを出力:

```bash
python -v setup.py --config config.yaml --output ../my-project
```

## ライセンス

このスクリプトは親リポジトリと同じライセンスです。
