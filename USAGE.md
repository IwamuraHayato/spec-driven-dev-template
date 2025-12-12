# テンプレート使用ガイド

このガイドでは、仕様駆動開発テンプレートを新規プロジェクトに適用する手順を説明します。

## 📋 前提条件

- Git がインストールされている
- テキストエディタ（VS Code 推奨）
- 基本的なコマンドライン操作の知識

## 🚀 クイックスタート（5分で完了）

### 1. テンプレートを取得

```bash
# テンプレートリポジトリをクローン
git clone https://github.com/IwamuraHayato/spec-driven-dev-template.git

# または、ダウンロードして解凍
# https://github.com/IwamuraHayato/spec-driven-dev-template/archive/main.zip
```

### 2. プロジェクトディレクトリを準備

```bash
# 新規プロジェクトディレクトリを作成
mkdir my-awesome-app
cd my-awesome-app

# Git 初期化
git init
```

### 3. 自動生成スクリプトを使用（推奨）

#### オプション A: 対話型セットアップ

```bash
cd /path/to/spec-driven-dev-template/generators/

# 依存関係のインストール
pip install -r requirements.txt

# 対話型セットアップを実行
python interactive_setup.py
```

質問に答えていくだけでプロジェクトが生成されます。

#### オプション B: 設定ファイルを使用

```bash
cd /path/to/spec-driven-dev-template/generators/

# 依存関係のインストール
pip install -r requirements.txt

# template-config.yaml を編集してから実行
python setup.py --config ../templates/nextjs-fastapi/template-config.yaml --output ../../my-new-project
```

**利用可能なオプション**:
- `--config`: 設定ファイルへのパス（必須）
- `--output`: 出力ディレクトリ（必須）
- `--template`: 使用するテンプレート（デフォルト: nextjs-fastapi）
- `--force`: 既存ディレクトリを上書き
- `--no-validate`: バリデーションをスキップ（非推奨）

---

## 📝 手動セットアップ（上級者向け）

自動化スクリプトを使わない場合の手順:

### 手動 1. テンプレートをコピー

```bash
# テンプレートファイルをコピー
cp -r /path/to/spec-driven-dev-template/templates/nextjs-fastapi/* .
cp -r /path/to/spec-driven-dev-template/templates/nextjs-fastapi/.* .
```

### 手動 2. 変数を置換

#### 手動置換

以下のファイルをテキストエディタで開き、`{{変数名}}` を実際の値に置換:

**必須置換ファイル:**
1. `CLAUDE.md.template` → `CLAUDE.md`
2. `README.md.template` → `README.md`
3. `docs/team-development-rules.md.template` → `docs/team-development-rules.md`
4. `docs/dev/REVIEW.md`
5. `.github/workflows/claude-pr-review.yml`

**置換する変数:**

| 変数名 | 例 | 説明 |
|--------|-----|------|
| `{{PROJECT_NAME}}` | `my-awesome-app` | プロジェクト名 |
| `{{PROJECT_DESCRIPTION}}` | `次世代 Web アプリケーション` | プロジェクト説明 |
| `{{REPOSITORY_URL}}` | `https://github.com/IwamuraHayato/my-awesome-app` | リポジトリ URL |
| `{{INFRASTRUCTURE_PLATFORM}}` | `AWS` / `GCP` / `Azure` | インフラプラットフォーム |
| `{{DATABASE_TYPE}}` | `PostgreSQL` / `MySQL` | データベースの種類 |
| `{{DATABASE_VERSION}}` | `14+` (PostgreSQL) / `8.0+` (MySQL) | データベースバージョン |
| `{{DATABASE_PORT}}` | `5432` (PostgreSQL) / `3306` (MySQL) | データベースポート番号 |
| `{{DATABASE_CLIENT_TOOLS}}` | `psql, pgAdmin, DBeaver` (PostgreSQL) / `mysql, MySQL Workbench, DBeaver` (MySQL) | データベースクライアントツール |
| `{{DATABASE_URL_EXAMPLE}}` | `postgresql+asyncpg://user:password@localhost:5432/dbname` (PostgreSQL) / `mysql+aiomysql://user:password@localhost:3306/dbname` (MySQL) | データベース接続 URL の例 |
| `{{ORGANIZATION_NAME}}` | `Your Company` | 組織名 |
| `{{PM_NAME}}` | `山田太郎` | プロジェクトマネージャー名 |
| `{{TECH_LEAD_NAME}}` | `鈴木花子` | 技術リード名 |
| `{{TARGET_USER_DESCRIPTION}}` | `エンドユーザー向けサービス利用者` | ターゲットユーザー説明 |
| `{{TEST_COVERAGE_TARGET}}` | `80` | テストカバレッジ目標(%) |
| `{{LICENSE}}` | `MIT` / `Apache 2.0` / `Proprietary` | ライセンス |
| `{{FEATURES_LIST}}` | リスト形式で機能を記載 | 主要機能リスト |

#### VS Code での一括置換方法

1. VS Code でプロジェクトフォルダを開く
2. `Cmd/Ctrl + Shift + H` で検索・置換パネルを開く
3. 検索モード切替: "正規表現" を有効化（`.*` アイコン）
4. 検索: `\{\{PROJECT_NAME\}\}`
5. 置換: `my-awesome-app`
6. "すべて置換" をクリック
7. 他の変数も同様に置換

### 5. テンプレートファイル名を変更

```bash
# .template 拡張子を削除
mv CLAUDE.md.template CLAUDE.md
mv README.md.template README.md
mv docs/team-development-rules.md.template docs/team-development-rules.md
```

### 6. 不要ファイルを削除

```bash
# テンプレート設定ファイルを削除（プロジェクトには不要）
rm template-config.yaml
```

### 7. Git コミット

```bash
git add .
git commit -m "chore: initial project setup from template"
```

## 📝 詳細設定

### CLAUDE.md のカスタマイズ

プロジェクト固有の情報を追加:

```markdown
## プロジェクト固有の機能

### 特殊な認証フロー
[プロジェクト独自の認証方法を記載]

### カスタムビジネスロジック
[特殊なビジネスルールを記載]
```

### GitHub Secrets の設定

Claude PR レビュー機能を有効化するには、GitHub リポジトリに Secret を追加:

1. GitHub リポジトリの Settings → Secrets and variables → Actions
2. "New repository secret" をクリック
3. Secret を追加:
   - Name: `ANTHROPIC_API_KEY`
   - Value: あなたの Claude API キー

### VS Code 拡張機能のインストール

```bash
# プロジェクトを VS Code で開く
code .

# VS Code が推奨拡張機能をインストールするよう促すので、"Install All" をクリック
```

または、コマンドラインから:

```bash
# .vscode/extensions.json に記載された拡張機能を一括インストール
code --install-extension esbenp.prettier-vscode
code --install-extension dbaeumer.vscode-eslint
code --install-extension charliermarsh.ruff
code --install-extension ms-python.python
code --install-extension bradlc.vscode-tailwindcss
```

## 🎨 機能別のカスタマイズ

### 1. コーディングスタイルのカスタマイズ

`.cursor/rules/code_style.mdc` を編集:

```markdown
- フロントエンド（Next.js/TypeScript）:
  - 独自ルール: インポート順序は外部 → 内部 → 相対パス
```

### 2. コミットメッセージのカスタマイズ

`.cursor/rules/commit_message.mdc` を編集:

```markdown
## 追加タイプ
- perf: パフォーマンス改善
- security: セキュリティ修正
```

### 3. Issue テンプレートの追加

`.github/ISSUE_TEMPLATE/` に新しいテンプレートを追加:

```markdown
---
name: Feature Request
about: 新機能の提案
title: "[FEATURE] "
labels: enhancement
assignees: ""
---

## 機能の概要
<!-- 提案する機能を説明 -->

## ユースケース
<!-- どのような場合に使用するか -->

## 期待される効果
<!-- この機能によって得られるメリット -->
```

### 4. GitHub Actions のカスタマイズ

`.github/workflows/pr-checks.yml` にカスタムチェックを追加:

```yaml
- name: Security scan
  run: npm audit
```

## 🔒 セキュリティ機能の活用

### セキュリティ規約の確認

テンプレートには IPA「安全なウェブサイトの作り方」準拠のセキュリティ規約が含まれています:

```bash
# セキュリティ規約を確認
cat .cursor/rules/security.mdc

# セキュリティチェックリストを確認
cat docs/security-checklist.md
```

### Cursor/Claude Code での活用

セキュリティ規約は `.cursor/rules/security.mdc` に配置されているため、Cursor や Claude Code が自動的に読み込みます:

- **開発時**: AIがセキュアなコードパターンを自動提案
- **レビュー時**: セキュリティ規約に基づいた自動チェック
- **実装時**: 脆弱性対策のコード例を参照可能

### セキュリティチェックリストの使用

開発フェーズごとにチェックリストを活用:

```markdown
## 実装フェーズ
- [ ] 1-1. SQL文の組み立ては、プレースホルダを用いて実装した
- [ ] 2-1. ファイルアクセスは、固定ディレクトリ配下に制限した
- [ ] 3-1. セッションIDは推測困難な値で生成した
...
```

詳細は [templates/nextjs-fastapi/docs/security/](templates/nextjs-fastapi/docs/security/) を参照してください。

---

## 🔍 検証

テンプレートが正しく適用されたか確認:

### チェックリスト

- [ ] `CLAUDE.md` にプロジェクト名が正しく記載されている
- [ ] `README.md` にプロジェクト説明が記載されている
- [ ] `.cursor/rules/` に **9 つのルールファイル**がある（security.mdc, python_coding.mdc を含む）
- [ ] `.github/ISSUE_TEMPLATE/` に Issue テンプレートがある
- [ ] `.github/PULL_REQUEST_TEMPLATE/` に PR テンプレートがある
- [ ] `.github/workflows/` に GitHub Actions ワークフローがある
- [ ] `.vscode/settings.json` に VS Code 設定がある
- [ ] `docs/dev/REVIEW.md` にレビューガイドラインがある
- [ ] `docs/team-development-rules.md` にチーム開発ルールがある
- [ ] `docs/security/` にセキュリティリファレンスがある
- [ ] `docs/security-checklist.md` にセキュリティチェックリストがある

### 動作確認

1. **VS Code でプロジェクトを開く**
   ```bash
   code .
   ```

2. **Cursor で開発規約が適用されるか確認**
   - `.cursor/rules/` のルールが自動的に読み込まれる

3. **GitHub Actions の動作確認**
   - ブランチを作成してダミーコミット
   ```bash
   git checkout -b test/verify-template
   echo "test" > test.txt
   git add test.txt
   git commit -m "test: verify template setup"
   git push origin test/verify-template
   ```
   - GitHub で PR を作成
   - GitHub Actions が自動実行されることを確認

## 🚨 トラブルシューティング

### 問題: 変数が置換されていない

**解決策**: すべてのテンプレートファイルで変数を確認

```bash
# 置換されていない変数を検索
grep -r "{{" .
```

### 問題: GitHub Actions が動作しない

**解決策**:
1. `ANTHROPIC_API_KEY` が正しく設定されているか確認
2. ワークフローファイルの YAML 構文エラーを確認
3. GitHub Actions のログを確認

### 問題: VS Code の拡張機能が動作しない

**解決策**:
1. 拡張機能が正しくインストールされているか確認
2. VS Code を再起動
3. `.vscode/settings.json` の構文エラーを確認

## 📚 次のステップ

テンプレート適用後:

1. **プロジェクト構造を作成**
   ```bash
   mkdir -p frontend/src/{app,components,lib,types}
   mkdir -p backend/app/{api,core,models,schemas,services}
   ```

2. **依存関係をインストール**
   ```bash
   cd frontend && npm init -y
   cd ../backend && python -m venv venv
   ```

3. **初回コミット**
   ```bash
   git add .
   git commit -m "chore: initial project structure"
   ```

4. **開発開始！**

## 🤝 サポート

質問や問題がある場合:

1. [GitHub Issues](https://github.com/IwamuraHayato/spec-driven-dev-template/issues) で質問
2. プロジェクトの `docs/team-development-rules.md` を参照
3. チームメンバーに相談

## 🔗 Spec Kit との併用

このテンプレートは [Spec Kit](https://github.com/github/spec-kit) と組み合わせて使用することで、仕様駆動開発の全フェーズをカバーできます。

### 役割分担

| ツール | 役割 | タイミング |
|---|---|---|
| **本テンプレート** | 開発環境・規約の初期化 | プロジェクト開始時（1回） |
| **Spec Kit** | 要件定義・設計・タスク化 | 機能追加ごと（繰り返し） |

### Spec Kit のインストール

```bash
# 推奨: 永続インストール
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# または一時使用
uvx --from git+https://github.com/github/spec-kit.git specify init .
```

### 併用フロー

```bash
# Step 1: 本テンプレートでプロジェクト初期化
git clone https://github.com/IwamuraHayato/spec-driven-dev-template.git
cd spec-driven-dev-template/generators/
pip install -r requirements.txt
python interactive_setup.py
# → .cursor/rules/, .github/, CLAUDE.md などが生成される

# Step 2: Spec Kit を初期化
cd ../my-new-project/
specify init . --ai claude --force
# → .speckit/, specs/ ディレクトリが追加される

# Step 3: 機能開発サイクル（繰り返し）
# Claude Code 上で実行:
/speckit.specify   # 要件定義
/speckit.plan      # 技術設計
/speckit.tasks     # タスク分解
/speckit.implement # 実装（.cursor/rules/ の規約に従う）
```

### 統合後のディレクトリ構造

```
my-project/
├── .speckit/                    # Spec Kit（プロジェクト原則）
│   └── constitution.md
├── specs/                       # Spec Kit（機能仕様）
│   └── feature-xxx/
│       ├── spec.md              # ユーザーストーリー・受け入れ基準
│       ├── plan.md              # 実装計画・フェーズ分割
│       ├── data-model.md        # エンティティ・スキーマ定義
│       ├── contracts/           # APIスキーマ・イベント定義
│       └── tasks.md             # 実行可能タスクリスト
├── .cursor/rules/               # 本テンプレート（コーディング規約）
├── .github/                     # 本テンプレート（Issue/PR/CI）
├── docs/                        # 本テンプレート（チームルール）
├── CLAUDE.md                    # 本テンプレート（AI指示書）
├── frontend/                    # 実装コード
└── backend/                     # 実装コード
```

### Spec Kit コマンド一覧

| コマンド | 目的 | 出力 |
|---|---|---|
| `/speckit.constitution` | プロジェクト原則の策定 | `.speckit/constitution.md` |
| `/speckit.specify` | 要件定義・ユーザーストーリー | `specs/[feature]/spec.md` |
| `/speckit.plan` | 技術設計・実装計画 | `specs/[feature]/plan.md` |
| `/speckit.tasks` | タスク分解 | `specs/[feature]/tasks.md` |
| `/speckit.implement` | 実装実行 | 実装コード |

詳細は [Spec Kit 公式リポジトリ](https://github.com/github/spec-kit) を参照してください。

## 📖 関連ドキュメント

- [README.md](README.md): テンプレートの概要
- [Spec Kit](https://github.com/github/spec-kit): 仕様駆動開発ツールキット
- [templates/nextjs-fastapi/CLAUDE.md.template](templates/nextjs-fastapi/CLAUDE.md.template): AI 向け指示書のサンプル
- [templates/nextjs-fastapi/docs/team-development-rules.md.template](templates/nextjs-fastapi/docs/team-development-rules.md.template): チーム開発ルールのサンプル
