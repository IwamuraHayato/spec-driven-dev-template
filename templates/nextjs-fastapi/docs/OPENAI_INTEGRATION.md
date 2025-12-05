# OpenAI 連携ガイド（オプション設定）

このドキュメントでは、Claude Code と OpenAI API を連携させて、バグ解析やコード理解を強化する方法を説明します。

> **注意**: この設定は**オプション**です。Claude Code 単体でも十分な開発が可能です。OpenAI API を活用したい場合のみ設定してください。

## Claude Code を使った設定サポート

このテンプレートを使用しているプロジェクトでは、**Claude Code が設定をサポート**します。

### 設定を開始する方法

Claude Code に以下のように依頼してください：

```
「OpenAI 連携を設定したい」
```

または

```
「OpenAI API を使いたい」
```

Claude Code が自動的にこのドキュメントを参照し、段階的に設定をサポートします。

### Claude Code がサポートする内容

1. **現在の状態確認**
   - OpenAI CLI のインストール確認
   - API キーの設定状況確認
   - MCP サーバーの接続状態確認

2. **API キー取得のガイド**
   - OpenAI Platform への誘導
   - 課金設定の説明
   - 安全な API キー管理方法の案内

3. **環境変数の設定**
   - セキュアな設定方法の提示
   - `~/.zshrc` への追加サポート
   - 設定の反映確認

4. **MCP サーバーのセットアップ**
   - 必要なファイルの自動作成
   - 依存関係のインストール
   - Claude Code への登録

5. **動作確認とテスト**
   - テストコードでの検証
   - トラブルシューティング

### 重要な安全対策

Claude Code は以下のセキュリティ対策を実施します：

- ⚠️ **API キーをチャットに貼り付けない**: 環境変数として安全に設定する方法を案内
- ✅ **段階的な確認**: 各ステップで動作確認を実施
- 🔒 **秘密情報の保護**: API キーは最初の数文字のみで確認

### 設定完了後の使い方

設定が完了すると、以下のように依頼できます：

```
「このコードを OpenAI で解析して」
「このバグを OpenAI に聞いて」
「このコードを OpenAI で改善して」
```

Claude Code が自動的に OpenAI GPT-5.1 に問い合わせ、結果を統合します。

## 概要

### 連携のメリット

- **Claude Code の利便性**: ファイル操作、Git連携、プロジェクト管理
- **OpenAI GPT-5.1 の技術力**: 高度なバグ解析、コード理解、別視点からの提案

### 使い分けの推奨

| タスク | 推奨ツール | 理由 |
|--------|-----------|------|
| 通常の開発作業 | Claude Code | 統合された開発体験 |
| 複雑なバグ解析 | OpenAI GPT-5.1 | 別視点からの深い分析 |
| コードレビュー | 両方併用 | 多角的な視点 |
| ファイル操作・Git | Claude Code | 自動化されたワークフロー |

## 前提条件

### 必要なもの

1. **OpenAI API アカウント**
   - URL: https://platform.openai.com/
   - ChatGPT Plus とは**別契約**（従量課金制）

2. **OpenAI CLI**
   - 通常は既にインストール済み
   - 確認: `openai --version`

3. **API キー**
   - OpenAI Platform で取得
   - 課金設定が必要

### コスト目安

| モデル | 1M tokens あたり | バグ修正1回の目安 |
|--------|-----------------|------------------|
| GPT-5.1 | $30入力/$60出力 | $0.01-0.05 |
| GPT-4 | $30入力/$60出力 | $0.01-0.05 |
| GPT-3.5-turbo | $1.5入力/$2出力 | $0.001-0.01 |

月額 $10 程度で十分な開発利用が可能です。

## セットアップ手順

### ステップ1: OpenAI API キーの取得

1. **OpenAI Platform にログイン**
   - https://platform.openai.com/

2. **課金設定**
   - 左サイドバー → "Billing"
   - "Add payment method" でクレジットカードを追加
   - "Usage limits" で月額上限を設定（推奨: $10-20/月）

3. **API キー作成**
   - 左サイドバー → "API keys"
   - "Create new secret key" をクリック
   - 名前: "Claude Code Integration"
   - キーをコピー（⚠️ 一度しか表示されません）

### ステップ2: API キーの設定

**重要**: API キーは機密情報です。チャットやコードに直接貼り付けないでください。

#### 環境変数として設定

```bash
# ~/.zshrc または ~/.bashrc に追加
nano ~/.zshrc
```

ファイルの最後に以下を追加：

```bash
export OPENAI_API_KEY="sk-proj-your-actual-key-here"
```

保存して反映：

```bash
source ~/.zshrc
```

#### 動作確認

```bash
echo $OPENAI_API_KEY | head -c 7
# "sk-proj" と表示されれば成功
```

### ステップ3: MCP サーバーの作成

#### ディレクトリ作成

```bash
mkdir -p ~/.claude/mcp-servers/openai-cli-bridge
cd ~/.claude/mcp-servers/openai-cli-bridge
```

#### サーバーコード作成

`server.js` ファイルを作成（コードは以下のセクション参照）

#### 依存関係のインストール

```bash
npm install
chmod +x server.js
```

### ステップ4: Claude Code に登録

```bash
claude mcp add --transport stdio openai-cli \
  -- node ~/.claude/mcp-servers/openai-cli-bridge/server.js
```

#### 確認

```bash
claude mcp list
```

以下のように表示されれば成功：

```
openai-cli: node ~/.claude/mcp-servers/openai-cli-bridge/server.js - ✓ Connected
```

## 使い方

### 基本的な使用方法

#### バグ解析

```
あなた: "このコードを OpenAI で解析して"
```

Claude Code が自動的に：
1. コードを読み込み
2. OpenAI GPT-5.1 に送信
3. 解析結果を受け取り
4. 修正案を提示

#### コード理解

```
あなた: "この複雑な関数を OpenAI で説明して"
```

GPT-5.1 がコードの詳細な説明を提供します。

#### コード改善

```
あなた: "このコードを OpenAI で改善して"
```

パフォーマンス、可読性、セキュリティの観点から改善提案を取得します。

### 実践例

#### 例1: バグ修正ワークフロー

```javascript
// バグのあるコード
function removeItem(itemName) {
  this.items = this.items.filter(item => item.name = itemName); // バグ
}
```

**依頼**:
```
「removeItem が動かない理由を OpenAI に聞いて」
```

**結果**:
- OpenAI が原因特定（`=` を `===` に）
- Claude Code が修正実装
- 動作確認まで完了

#### 例2: セカンドオピニオン

```
「このリファクタリングを OpenAI でレビューして」
```

Claude Code の実装を OpenAI で検証し、より良い提案があれば取り入れます。

## トラブルシューティング

### API キーが認識されない

```bash
# 環境変数を再読み込み
source ~/.zshrc

# 確認
echo $OPENAI_API_KEY | head -c 7
```

### クォータエラー (Error 429)

```
Error code: 429 - insufficient_quota
```

**原因**: 課金設定が未完了、または利用上限到達

**解決方法**:
1. https://platform.openai.com/settings/organization/billing にアクセス
2. 支払い方法を確認
3. 利用上限を確認・調整

### モデルが使えない (Error 404)

一部のモデルは chat completions エンドポイントに非対応です。

**対応モデル**:
- ✅ gpt-5.1（推奨）
- ✅ gpt-4
- ✅ gpt-3.5-turbo
- ❌ gpt-5.1-codex（completions のみ）

## モデルの変更

### デフォルト: GPT-5.1

`~/.claude/mcp-servers/openai-cli-bridge/server.js` の137行目：

```javascript
const command = `openai api chat.completions.create -m gpt-5.1 -g user '${escapedPrompt}'`;
```

### コスト重視: GPT-3.5-turbo に変更

```javascript
const command = `openai api chat.completions.create -m gpt-3.5-turbo -g user '${escapedPrompt}'`;
```

変更後、Claude Code を再起動してください。

## セキュリティのベストプラクティス

### API キーの管理

- ✅ 環境変数に保存
- ✅ `.gitignore` で `.env` を除外
- ❌ コードに直接記述しない
- ❌ チャットに貼り付けない
- ❌ GitHub にコミットしない

### 利用上限の設定

OpenAI Platform で月額上限を設定：

1. "Usage limits" にアクセス
2. "Hard limit" を設定（例: $10/月）
3. "Soft limit" で通知設定（例: $5 で警告）

## よくある質問

### Q: ChatGPT Plus があれば API は不要？

**A**: いいえ、別物です。ChatGPT Plus は Web UI の定額サービスで、API は別途契約が必要です。

### Q: Claude Code だけでは不十分？

**A**: いいえ、Claude Code 単体で十分です。この連携は**オプション**で、別視点が欲しい場合のみ有用です。

### Q: いつ OpenAI を使うべき？

**A**: 以下の場合に有用です：
- 非常に複雑なバグで別視点が必要
- Claude Code の提案に不安がある
- セカンドオピニオンが欲しい
- 特定の専門領域（暗号、アルゴリズム等）

### Q: コストが心配

**A**: 月額上限を設定すれば安心です：
- $5/月: 軽い使用
- $10/月: 通常の開発
- $20/月: 頻繁な使用

バグ修正1回あたり $0.01-0.05 程度です。

## まとめ

### この連携により実現できること

✅ **Claude Code の利便性** × **OpenAI の技術力**
✅ **シームレスな統合**: 1つのチャットで両方のAIを活用
✅ **多角的な視点**: より確実な開発判断

### 推奨ワークフロー

1. **通常の開発**: Claude Code が全て処理
2. **複雑な問題**: 「OpenAI で〜」と依頼して別視点を取得
3. **実装**: Claude Code が OpenAI の提案を実装

### サポート

問題が発生した場合：
1. MCP サーバーログ確認: `claude mcp list`
2. API キー確認: `echo $OPENAI_API_KEY`
3. OpenAI Platform で利用状況確認

---

**作成日**: 2025-12-06
**対象環境**: macOS, Claude Code with MCP
**OpenAI モデル**: GPT-5.1（推奨）
