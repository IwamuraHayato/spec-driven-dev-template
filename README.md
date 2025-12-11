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
- `docs/OPENAI_INTEGRATION.md`: OpenAI 連携ガイド（オプション）

### 6. 設定ファイル
- `template-config.yaml`: プロジェクト変数定義

## 🚀 使い方

### クイックスタート

```bash
# 1. テンプレートをクローン
git clone https://github.com/IwamuraHayato/spec-driven-dev-template.git
cd spec-driven-dev-template/generators/

# 2. 依存関係をインストール
pip install -r requirements.txt

# 3. 対話型セットアップを実行
python interactive_setup.py
```

質問に答えていくだけで、**30秒〜2分**でプロジェクトが自動生成されます。

詳細な使い方、手動セットアップ、カスタマイズ方法については **[USAGE.md](USAGE.md)** を参照してください。

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
└── generators/                   # 自動生成スクリプト（✅ Phase 2完成）
    ├── interactive_setup.py      # 対話型セットアップ
    ├── setup.py                  # メイン生成スクリプト
    ├── config_loader.py          # 設定ファイルローダー
    ├── template_processor.py     # テンプレート処理エンジン
    ├── validators.py             # 設定値バリデーター
    └── requirements.txt          # Python依存関係
```

## 🎯 このテンプレートが解決する問題

### Before (テンプレートなし)

- ❌ 各プロジェクトでゼロから設定ファイルを作成
- ❌ コーディングスタイルがバラバラ
- ❌ コミットメッセージが統一されていない
- ❌ レビュー基準が曖昧
- ❌ AI が適切にコードを生成できない

### After (テンプレートあり)

- ✅ **30秒-2分**でプロジェクトセットアップ完了（**90%以上の時間削減**）
- ✅ 統一されたコーディングスタイル
- ✅ 明確なコミットメッセージ規約
- ✅ 体系化されたレビュープロセス
- ✅ AI が規約に従ったコードを自動生成
- ✅ 対話型セットアップで初心者でも簡単

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

## 🔗 Spec Kit との併用（推奨）

このテンプレートは [Spec Kit](https://github.com/github/spec-kit) と組み合わせて使用することで、仕様駆動開発の全フェーズをカバーできます。

| ツール | 役割 | タイミング |
|---|---|---|
| **本テンプレート** | 開発環境・規約の初期化 | プロジェクト開始時（1回） |
| **Spec Kit** | 要件定義・設計・タスク化 | 機能追加ごと（繰り返し） |

```
本テンプレート          Spec Kit
     │                    │
     ▼                    ▼
「どう開発するか」     「何を開発するか」
 (規約・環境)          (要件・設計・タスク)
```

併用フロー、インストール方法、統合後のディレクトリ構造については **[USAGE.md](USAGE.md#-spec-kit-との併用)** を参照してください。

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

- [Spec Kit](https://github.com/github/spec-kit) - 仕様駆動開発ツールキット
- [Next.js 公式ドキュメント](https://nextjs.org/docs)
- [FastAPI 公式ドキュメント](https://fastapi.tiangolo.com/)
- [Claude Code](https://claude.ai/code)
- [Cursor](https://cursor.sh/)

## 📧 お問い合わせ

質問や提案がある場合は、Issue を作成してください。
