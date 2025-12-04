# MySQL 対応完了サマリー

## 概要

テンプレートが PostgreSQL だけでなく MySQL にも対応しました。データベースの種類を変数で柔軟に切り替えられるようになりました。

## 変更内容

### 1. 新規追加変数 (5つ)

以下の変数を追加して、データベース固有の設定を柔軟に変更できるようにしました:

| 変数名 | PostgreSQL の例 | MySQL の例 |
|--------|-----------------|-----------|
| `{{DATABASE_TYPE}}` | `PostgreSQL` | `MySQL` |
| `{{DATABASE_VERSION}}` | `14+` | `8.0+` |
| `{{DATABASE_PORT}}` | `5432` | `3306` |
| `{{DATABASE_CLIENT_TOOLS}}` | `psql, pgAdmin, DBeaver` | `mysql, MySQL Workbench, DBeaver` |
| `{{DATABASE_URL_EXAMPLE}}` | `postgresql+asyncpg://user:password@localhost:5432/dbname` | `mysql+aiomysql://user:password@localhost:3306/dbname` |

### 2. 更新したファイル (7ファイル)

#### テンプレートファイル
1. **CLAUDE.md.template**
   - データベース技術スタック: `PostgreSQL 14+` → `{{DATABASE_TYPE}} {{DATABASE_VERSION}}`
   - アーキテクチャ図のデータベース表記
   - データフロー説明
   - セットアップ前提条件
   - トラブルシューティング (ポート競合、接続エラー)
   - デバッグ方法 (データベースクライアントツール)
   - 環境変数例 (DATABASE_URL)

2. **README.md.template**
   - 技術スタック: `PostgreSQL 14+` → `{{DATABASE_TYPE}} {{DATABASE_VERSION}}`
   - セットアップ前提条件
   - 環境変数設定例 (DATABASE_URL)
   - トラブルシューティング (ポート競合、接続エラー)

3. **docs/dev/REVIEW.md**
   - 技術スタック: `PostgreSQL` → `{{DATABASE_TYPE}}`

4. **docs/team-development-rules.md.template**
   - 外部リソース: PostgreSQL と MySQL の両方のドキュメントリンクを追加

5. **template-config.yaml**
   - データベース設定セクションを拡張
   - 各変数にコメントで PostgreSQL/MySQL の例を追加

#### ドキュメントファイル
6. **README.md** (リポジトリルート)
   - 置換が必要な変数リストにデータベース関連変数を追加

7. **USAGE.md**
   - 変数リスト表にデータベース関連変数を追加 (5つ)

8. **CHANGELOG.md**
   - Technical Stack セクションに MySQL 対応を明記
   - データベース柔軟性に関する説明を追加

## 使い方

### PostgreSQL を使用する場合

```yaml
# template-config.yaml
database:
  primary: "PostgreSQL"
  version: "14+"
  port: "5432"
  client_tools: "psql, pgAdmin, DBeaver"
  url_example: "postgresql+asyncpg://user:password@localhost:5432/dbname"
```

### MySQL を使用する場合

```yaml
# template-config.yaml
database:
  primary: "MySQL"
  version: "8.0+"
  port: "3306"
  client_tools: "mysql, MySQL Workbench, DBeaver"
  url_example: "mysql+aiomysql://user:password@localhost:3306/dbname"
```

## 置換方法

### VS Code での一括置換

1. VS Code でプロジェクトフォルダを開く
2. `Cmd/Ctrl + Shift + H` で検索・置換パネルを開く
3. 正規表現モードを有効化（`.*` アイコン）
4. 以下のように順次置換:

```
検索: \{\{DATABASE_TYPE\}\}
置換: MySQL (または PostgreSQL)

検索: \{\{DATABASE_VERSION\}\}
置換: 8.0+ (または 14+)

検索: \{\{DATABASE_PORT\}\}
置換: 3306 (または 5432)

検索: \{\{DATABASE_CLIENT_TOOLS\}\}
置換: mysql, MySQL Workbench, DBeaver (または psql, pgAdmin, DBeaver)

検索: \{\{DATABASE_URL_EXAMPLE\}\}
置換: mysql+aiomysql://user:password@localhost:3306/dbname
      (または postgresql+asyncpg://user:password@localhost:5432/dbname)
```

## 検証

すべてのテンプレートファイルから PostgreSQL 固有の記述を削除し、変数に置換しました:

```bash
# 検証コマンド (PostgreSQL/postgres の固有記述が残っていないことを確認)
grep -ri "postgresql\|postgres" templates/nextjs-fastapi/*.template
grep -ri "postgresql\|postgres" templates/nextjs-fastapi/docs/*.md
grep -ri "postgresql\|postgres" templates/nextjs-fastapi/.github/**/*.md

# 結果: コメント内の例のみ (問題なし)
```

## SQLAlchemy ドライバー

### PostgreSQL
- **非同期**: `asyncpg` (推奨)
- **同期**: `psycopg2`
- **接続 URL**: `postgresql+asyncpg://user:password@localhost:5432/dbname`

### MySQL
- **非同期**: `aiomysql` (推奨)
- **同期**: `pymysql`
- **接続 URL**: `mysql+aiomysql://user:password@localhost:3306/dbname`

## 注意事項

1. **マイグレーション**: Alembic は PostgreSQL と MySQL の両方に対応していますが、データ型の違いに注意が必要です
2. **SQL 方言**: 一部の SQL クエリは PostgreSQL と MySQL で構文が異なる場合があります (例: `SERIAL` vs `AUTO_INCREMENT`)
3. **依存関係**: `requirements.txt` に適切なドライバーを追加してください:
   - PostgreSQL: `asyncpg`
   - MySQL: `aiomysql`

## 完了ステータス

- [x] 変数定義 (template-config.yaml)
- [x] CLAUDE.md.template の更新
- [x] README.md.template の更新
- [x] docs/dev/REVIEW.md の更新
- [x] docs/team-development-rules.md.template の更新
- [x] ルートドキュメント (README.md, USAGE.md, CHANGELOG.md) の更新
- [x] 検証 (PostgreSQL 固有記述の確認)
- [x] ドキュメント作成 (このファイル)

## 今後の拡張

将来的に他のデータベースにも対応可能:
- SQLite (開発環境)
- MariaDB (MySQL 互換)
- CockroachDB (PostgreSQL 互換)

同じ変数システムを使用して、簡単に追加できます。
