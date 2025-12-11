# セキュリティCI/CD実装ガイド

IPA「安全なウェブサイトの作り方 第7版」に準拠したセキュリティチェックの自動化実装です。

**📦 自動統合**: プロジェクト生成時に自動的にセキュリティファイルが統合されます。

## 📋 目次

- [概要](#概要)
- [アーキテクチャ](#アーキテクチャ)
- [Phase 1: 静的解析ツール](#phase-1-静的解析ツール)
- [Phase 2: GitHub Actions](#phase-2-github-actions)
- [ローカルでの実行方法](#ローカルでの実行方法)
- [トラブルシューティング](#トラブルシューティング)

---

## アーキテクチャ

### ハイブリッド方式による複数テンプレート対応

```
spec-driven-dev-template/
├── .security-template/          # 共通セキュリティテンプレート
│   ├── .bandit
│   ├── .github/workflows/
│   └── scripts/security/
│
├── templates/
│   ├── nextjs-fastapi/
│   │   └── .security-config.yaml  # テンプレート固有設定
│   ├── django-react/              # 将来の追加テンプレート
│   │   └── .security-config.yaml
│   └── flask-vue/
│       └── .security-config.yaml
│
└── generators/
    └── security_integrator.py     # 自動統合スクリプト
```

### プロジェクト生成時の自動統合

`generators/interactive_setup.py` 実行時に以下が自動実行されます：

1. `.security-template/` から共通ファイルをコピー
2. テンプレート固有の `.security-config.yaml` を適用
3. `docs/security/README.md` を生成
4. 実行可能権限を設定

---

## 概要

このセキュリティCI/CDシステムは以下を自動化します：

- **Python**: Bandit + Semgrep によるセキュリティチェック
- **TypeScript/JavaScript**: Semgrep によるセキュリティチェック
- **PR自動コメント**: 検出された脆弱性をPRに自動投稿
- **IPAガイドライン準拠**: 11種類の脆弱性を検出

### 検出可能な脆弱性（IPA対応）

| IPA項目 | 脆弱性 | 検出ツール |
|---------|--------|------------|
| 1-(i) | SQLインジェクション | Bandit, Semgrep |
| 2-(i) | OSコマンドインジェクション | Bandit, Semgrep |
| 3-(i) | ディレクトリトラバーサル | Semgrep |
| 4-(i)(iii) | セッション管理の不備 | Semgrep |
| 5-(i)(ii)(iii) | XSS（クロスサイトスクリプティング） | Semgrep |
| 6-(i) | CSRF | Semgrep |
| 7-(i) | HTTPヘッダインジェクション | Semgrep |
| 8-(i) | メールヘッダインジェクション | Semgrep |
| - | 機密情報のハードコード | Bandit, Semgrep |
| - | 弱い暗号化 | Bandit, Semgrep |
| - | その他のセキュリティベストプラクティス | Bandit, Semgrep |

---

## Phase 1: 静的解析ツール

### ファイル構成

```
.
├── .bandit                                  # Bandit設定
├── scripts/
│   └── security/
│       ├── semgrep-rules/
│       │   ├── ipa-python.yaml             # Python用IPAルール
│       │   └── ipa-typescript.yaml         # TypeScript用IPAルール
│       ├── run-security-check.sh           # ローカル実行スクリプト
│       ├── generate-pr-comment.py          # PRコメント生成
│       └── check-critical-issues.py        # 重大問題チェック
```

### ツールのインストール

#### Python環境

```bash
# Bandit: Pythonセキュリティチェッカー
pip install bandit

# Semgrep: 多言語対応の静的解析ツール
pip install semgrep

# または Homebrew
brew install semgrep
```

#### 動作確認

```bash
# Bandit
bandit --version

# Semgrep
semgrep --version
```

---

## Phase 2: GitHub Actions

### ワークフロー構成

`.github/workflows/security-check.yml` が以下のジョブを実行します：

1. **python-security**: Python向けセキュリティチェック
   - Bandit実行
   - Semgrep (Python) 実行
   - 結果をアーティファクトに保存

2. **typescript-security**: TypeScript/JavaScript向けセキュリティチェック
   - Semgrep (TypeScript) 実行
   - 結果をアーティファクトに保存

3. **security-report**: 結果の集約とPR投稿
   - 各ジョブの結果を集約
   - PRコメントとして投稿
   - 重大な問題があればCIを失敗させる

### トリガー条件

- **ブランチ**: `main`, `develop` へのPR
- **対象ファイル**: `.py`, `.ts`, `.tsx`, `.js`, `.jsx`
- **設定変更**: `.bandit`, `scripts/security/**`, ワークフローファイル自体

### PRコメント例

```markdown
## 🔒 Security Check Results

🔴 **2件の重大な問題が検出されました**

---

### 🐍 Python Security (2 issues)

#### Bandit Results (1 issues)

| Severity | Rule | File | Line | Message |
|----------|------|------|------|----------|
| 🔴 HIGH | B608 | `api/users.py` | 45 | Possible SQL injection vector... |

#### Semgrep (Python) Results (1 issues)

| Severity | IPA | Rule | File | Line | Message |
|----------|-----|------|------|------|----------|
| 🔴 ERROR | 2-(i) | ipa-os-command-injection-shell-true | `utils/file.py` | 23 | OS command injection detected... |

---

### 📘 TypeScript/JavaScript Security

✅ No issues found

---

### 📚 References

- 📖 [セキュリティ規約](./templates/nextjs-fastapi/.cursor/rules/security.mdc)
- ✅ [セキュリティチェックリスト](./templates/nextjs-fastapi/docs/security-checklist.md)
- 🔗 [IPA 安全なウェブサイトの作り方](https://www.ipa.go.jp/security/vuln/websecurity/)
```

---

## ローカルでの実行方法

### 1. クイック実行（推奨）

```bash
# すべてのセキュリティチェックを実行
./scripts/security/run-security-check.sh
```

このスクリプトは以下を実行します：
- Banditチェック
- Semgrep (Python) チェック
- Semgrep (TypeScript) チェック
- 結果の集約と表示

### 2. 個別実行

#### Bandit のみ

```bash
# 標準出力に結果表示
bandit -r . -c .bandit

# JSON形式で出力
bandit -r . -c .bandit -f json -o bandit-results.json
```

#### Semgrep (Python) のみ

```bash
# 標準出力に結果表示
semgrep --config scripts/security/semgrep-rules/ipa-python.yaml .

# JSON形式で出力
semgrep --config scripts/security/semgrep-rules/ipa-python.yaml \
        --json --output semgrep-python-results.json .
```

#### Semgrep (TypeScript) のみ

```bash
# 標準出力に結果表示
semgrep --config scripts/security/semgrep-rules/ipa-typescript.yaml .

# JSON形式で出力
semgrep --config scripts/security/semgrep-rules/ipa-typescript.yaml \
        --json --output semgrep-typescript-results.json .
```

### 3. 特定のディレクトリのみチェック

```bash
# Pythonバックエンドのみ
bandit -r ./backend -c .bandit
semgrep --config scripts/security/semgrep-rules/ipa-python.yaml ./backend

# TypeScriptフロントエンドのみ
semgrep --config scripts/security/semgrep-rules/ipa-typescript.yaml ./frontend
```

---

## トラブルシューティング

### False Positive（誤検知）の除外

#### Bandit

`.bandit` ファイルで除外設定を追加：

```ini
[bandit]
# 特定のディレクトリを除外
exclude_dirs = ['/tests', '/migrations']

# 特定のテストを無効化
skips = ['B201', 'B301']
```

コード内でコメントを使用：

```python
# nosec B608
query = f"SELECT * FROM users WHERE id = {user_id}"
```

#### Semgrep

`.semgrepignore` ファイルを作成：

```
# テストファイルを除外
tests/
**/*_test.py
**/*.test.ts
```

コード内でコメントを使用：

```typescript
// nosemgrep: ipa-xss-dangerously-set-inner-html
<div dangerouslySetInnerHTML={{__html: trustedContent}} />
```

### よくあるエラー

#### 1. `bandit: command not found`

```bash
# Banditをインストール
pip install bandit
```

#### 2. `semgrep: command not found`

```bash
# Semgrepをインストール
pip install semgrep
# または
brew install semgrep
```

#### 3. GitHub Actionsでのパーミッションエラー

ワークフローファイルの `permissions` セクションを確認：

```yaml
permissions:
  contents: read
  pull-requests: write
  security-events: write
```

#### 4. PRコメントが投稿されない

- GitHub Actionsの実行ログを確認
- `GITHUB_TOKEN` の権限を確認
- アーティファクトが正しくダウンロードされているか確認

---

## 次のステップ

### Phase 3: AIセキュリティレビュー（予定）

- Claude APIを使用した高度なセキュリティレビュー
- 静的解析では検出できないロジックの脆弱性を検出
- Issue #15 を参照

### Phase 4: チェックリスト自動更新（予定）

- セキュリティチェック結果に基づくチェックリストの自動更新
- 対応済み項目の自動マーク
- Issue #16 を参照（未作成）

---

## 参考資料

- [IPA 安全なウェブサイトの作り方](https://www.ipa.go.jp/security/vuln/websecurity/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Semgrep Documentation](https://semgrep.dev/docs/)
- [セキュリティ規約](../../templates/nextjs-fastapi/.cursor/rules/security.mdc)
- [セキュリティチェックリスト](../../templates/nextjs-fastapi/docs/security-checklist.md)

---

## 関連イシュー

- #12 [Epic] IPAセキュリティガイドライン準拠のCI/CD実装
- #13 [Security] Phase 1: 静的解析ツールの導入
- #14 [Security] Phase 2: GitHub Actionsワークフロー作成
- #15 [Security] Phase 3: AIセキュリティレビュー実装
