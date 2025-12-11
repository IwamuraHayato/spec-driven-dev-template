# セキュリティCI/CD実装計画

本ドキュメントはGitHubイシュー作成用のテンプレートです。

---

## Epic Issue（親イシュー）

### タイトル
```
[Epic] IPAセキュリティガイドライン準拠のCI/CD実装
```

### 本文
```markdown
## 概要

IPA「安全なウェブサイトの作り方 第7版」に基づくセキュリティチェックをCI/CDパイプラインに組み込み、開発フロー全体でセキュリティを担保する仕組みを構築する。

## 背景

- セキュリティ規約（security.mdc）とチェックリスト（security-checklist.md）を作成済み
- これらを開発フローに組み込み、自動チェックを実現したい
- AIドリブン開発でチェックリストを自動更新したい

## ゴール

1. PR作成時に自動でセキュリティチェックが実行される
2. 検出された問題がPRコメントとして報告される
3. チェックリストが自動更新される
4. 開発者がセキュリティを意識しなくても安全なコードが書ける

## 実装フェーズ

- [ ] Phase 1: 静的解析ツールの導入 #XX
- [ ] Phase 2: GitHub Actionsワークフロー作成 #XX
- [ ] Phase 3: AIセキュリティレビュー実装 #XX
- [ ] Phase 4: チェックリスト自動更新機能 #XX

## 対象言語

- Python（FastAPI）
- TypeScript（Next.js）

## 関連ファイル

- `.cursor/rules/security.mdc` - セキュリティ規約
- `docs/security-checklist.md` - チェックリスト

## 参考資料

- [IPA 安全なウェブサイトの作り方](https://www.ipa.go.jp/security/vuln/websecurity/)
```

### ラベル
- `enhancement`
- `security`
- `epic`

---

## Phase 1 Issue

### タイトル
```
[Security] Phase 1: 静的解析ツールの導入
```

### 本文
```markdown
## 概要

IPAセキュリティガイドラインに基づく静的解析ツールを導入する。

## 親イシュー

- #XX [Epic] IPAセキュリティガイドライン準拠のCI/CD実装

## タスク

### Python（FastAPI）

- [ ] Bandit の設定ファイル作成（`.bandit`）
- [ ] Semgrep カスタムルール作成（IPA準拠）
  - [ ] 1. SQLインジェクション検出
  - [ ] 2. OSコマンドインジェクション検出
  - [ ] 3. ディレクトリトラバーサル検出
  - [ ] 4. ハードコード秘密情報検出

### TypeScript（Next.js）

- [ ] ESLint Security Plugin 導入
- [ ] Semgrep カスタムルール作成（IPA準拠）
  - [ ] 5. XSS（dangerouslySetInnerHTML）検出
  - [ ] 6. URLスキーム検証
  - [ ] 7. eval/Function使用検出

### 設定ファイル

```
scripts/
└── security/
    └── semgrep-rules/
        ├── ipa-python.yaml      # Python用ルール
        └── ipa-typescript.yaml  # TypeScript用ルール
```

## 検出対象（IPAチェックリスト対応）

| IPA項目 | 検出内容 | ツール |
|---------|----------|--------|
| 1-(i) | SQLインジェクション | Bandit, Semgrep |
| 2-(i) | OSコマンドインジェクション | Bandit, Semgrep |
| 3-(i) | ディレクトリトラバーサル | Semgrep |
| 5-(i) | XSS | ESLint, Semgrep |
| 5-(iii) | script動的生成 | ESLint, Semgrep |

## 受け入れ条件

- [ ] ローカルで静的解析が実行できる
- [ ] サンプルの脆弱なコードで検出を確認
- [ ] 既存コードでfalse positiveが許容範囲内
```

### ラベル
- `enhancement`
- `security`
- `phase-1`

---

## Phase 2 Issue

### タイトル
```
[Security] Phase 2: GitHub Actionsワークフロー作成
```

### 本文
```markdown
## 概要

Phase 1で導入した静的解析ツールをGitHub Actionsで自動実行する。

## 親イシュー

- #XX [Epic] IPAセキュリティガイドライン準拠のCI/CD実装

## 依存

- #XX Phase 1: 静的解析ツールの導入

## タスク

### ワークフロー作成

- [ ] `.github/workflows/security-check.yml` 作成
- [ ] PRトリガー設定（main, develop向け）
- [ ] パス フィルター設定（backend/, frontend/）

### ジョブ構成

```yaml
jobs:
  python-security:    # Bandit + Semgrep
  typescript-security: # ESLint + Semgrep
  security-report:    # 結果集約・コメント投稿
```

### 機能要件

- [ ] Python静的解析ジョブ
  - [ ] Bandit 実行
  - [ ] Semgrep 実行（Python用ルール）
  - [ ] 結果をアーティファクトに保存

- [ ] TypeScript静的解析ジョブ
  - [ ] ESLint Security 実行
  - [ ] Semgrep 実行（TypeScript用ルール）
  - [ ] 結果をアーティファクトに保存

- [ ] レポートジョブ
  - [ ] 各ジョブの結果を集約
  - [ ] PRコメントとして投稿
  - [ ] 重大な問題があればCIを失敗させる

## PRコメント形式

```markdown
## 🔒 Security Check Results

### Python (Bandit + Semgrep)
⚠️ 2 issues found

| Severity | Rule | File | Line | Message |
|----------|------|------|------|---------|
| HIGH | IPA-1-(i) | api/users.py | 45 | SQL injection detected |

### TypeScript (ESLint + Semgrep)
✅ No issues found

---
📋 [セキュリティチェックリスト](./docs/security-checklist.md)
```

## 受け入れ条件

- [ ] PR作成時に自動でセキュリティチェックが実行される
- [ ] 結果がPRコメントとして投稿される
- [ ] HIGH/CRITICALの問題があればCIが失敗する
- [ ] 結果がアーティファクトとしてダウンロード可能
```

### ラベル
- `enhancement`
- `security`
- `ci-cd`
- `phase-2`

---

## Phase 3 Issue

### タイトル
```
[Security] Phase 3: AIセキュリティレビュー実装
```

### 本文
```markdown
## 概要

Claude APIを使用して、PR差分に対するAIセキュリティレビューを実装する。
静的解析では検出できない複雑なロジックの脆弱性を検出する。

## 親イシュー

- #XX [Epic] IPAセキュリティガイドライン準拠のCI/CD実装

## 依存

- #XX Phase 2: GitHub Actionsワークフロー作成

## 前提条件

- Claude API キーの取得（または Claude Code MAX のCI対応を待つ）
- GitHub Secrets に `ANTHROPIC_API_KEY` を設定

## タスク

### スクリプト作成

- [ ] `scripts/security/ai-security-review.py` 作成
  - [ ] PR差分の取得機能
  - [ ] security.mdc の読み込み
  - [ ] Claude APIへのリクエスト
  - [ ] レビュー結果のパース

### ワークフロー更新

- [ ] `security-check.yml` に AI レビュージョブ追加
- [ ] 静的解析と並列実行
- [ ] 結果をレポートに統合

### プロンプト設計

```
入力:
- security.mdc（セキュリティガイドライン）
- security-checklist.md（チェックリスト）
- PR差分（変更されたファイル）

出力:
- 検出された問題のリスト
- 該当するチェックリスト項目
- 改善提案
```

## AIレビューの対象

| 項目 | 静的解析 | AIレビュー |
|------|:--------:|:----------:|
| SQLインジェクション | ✅ | ✅ 複雑なケース |
| 認証・認可ロジック | ❌ | ✅ |
| ビジネスロジックの脆弱性 | ❌ | ✅ |
| セッション管理 | △ | ✅ |
| CSRF対策の妥当性 | ❌ | ✅ |

## コスト考慮

- Claude Sonnet使用を推奨（コスト効率）
- 差分のみをレビュー対象に（トークン節約）
- 大きなPRは警告を出す（手動レビュー推奨）

## 受け入れ条件

- [ ] PR作成時にAIレビューが自動実行される
- [ ] security.mdcに基づいたレビューが行われる
- [ ] 結果がPRコメントとして投稿される
- [ ] APIエラー時もCIが失敗しない（静的解析は継続）
```

### ラベル
- `enhancement`
- `security`
- `ai`
- `phase-3`

---

## Phase 4 Issue

### タイトル
```
[Security] Phase 4: チェックリスト自動更新機能
```

### 本文
```markdown
## 概要

セキュリティチェックの結果に基づいて、security-checklist.md を自動更新する機能を実装する。

## 親イシュー

- #XX [Epic] IPAセキュリティガイドライン準拠のCI/CD実装

## 依存

- #XX Phase 3: AIセキュリティレビュー実装

## タスク

### スクリプト作成

- [ ] `scripts/security/update-checklist.py` 作成
  - [ ] チェックリストの読み込み・パース
  - [ ] ステータス更新ロジック
  - [ ] 更新後のファイル書き込み
  - [ ] 変更差分の生成

### 自動更新ルール

```python
# 更新ルール
rules = {
    # 静的解析で問題なし → 対応済み候補
    "no_issues": "suggest_done",

    # 静的解析で問題検出 → 未対策のまま
    "issues_found": "keep_pending",

    # 該当機能なし → 対応不要候補
    "not_applicable": "suggest_na",
}
```

### ワークフロー更新

- [ ] チェックリスト更新ジョブ追加
- [ ] 更新内容をPRコメントに含める
- [ ] 自動コミット機能（オプション）

### PRコメント形式

```markdown
## 📋 チェックリスト更新提案

### 対応済みに変更可能
以下の項目は対策が確認されました：
- `1-(i)-a` SQL文の組み立てにプレースホルダを使用
- `5-(viii)` Content-Typeにcharsetを指定

### 未対策のまま
以下の項目は対策が確認できませんでした：
- `4-(iii)` Cookieのsecure属性（該当コードなし）

### 自動更新を適用する場合
以下のコマンドを実行してください：
\`\`\`bash
python scripts/security/update-checklist.py --apply
\`\`\`
```

## 更新フロー

```
1. セキュリティチェック実行
       ↓
2. 結果を分析
       ↓
3. チェックリスト項目と照合
       ↓
4. 更新提案を生成
       ↓
5. PRコメントに投稿
       ↓
6. （オプション）自動コミット
```

## 受け入れ条件

- [ ] 静的解析結果に基づいてチェックリスト更新が提案される
- [ ] AIレビュー結果も反映される
- [ ] 手動承認後に更新が適用される
- [ ] 更新履歴がメタデータに記録される
```

### ラベル
- `enhancement`
- `security`
- `automation`
- `phase-4`

---

## イシュー作成手順

1. GitHubリポジトリの Issues タブを開く
2. 「New issue」をクリック
3. 上記の内容をコピー&ペースト
4. 適切なラベルを設定
5. Epic Issue 作成後、各 Phase Issue の「親イシュー」に番号を記入

## 推奨作成順序

1. Epic Issue を作成（番号を控える）
2. Phase 1 Issue を作成
3. Phase 2 Issue を作成
4. Phase 3 Issue を作成
5. Phase 4 Issue を作成
6. Epic Issue を編集し、各 Phase の番号を追記
