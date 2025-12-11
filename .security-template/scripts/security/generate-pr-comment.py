#!/usr/bin/env python3
"""
PRコメント生成スクリプト
セキュリティチェック結果を集約してMarkdown形式のコメントを生成
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict


def load_json_results(file_path: Path) -> Dict[str, Any]:
    """JSON結果ファイルを読み込む"""
    if not file_path.exists():
        return {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def parse_bandit_results(results: Dict[str, Any]) -> List[Dict[str, str]]:
    """Bandit結果をパース"""
    issues = []
    for result in results.get('results', []):
        issues.append({
            'severity': result.get('issue_severity', 'UNKNOWN'),
            'confidence': result.get('issue_confidence', 'UNKNOWN'),
            'rule': result.get('test_id', 'Unknown'),
            'file': result.get('filename', 'Unknown'),
            'line': result.get('line_number', '?'),
            'message': result.get('issue_text', 'No description'),
            'code': result.get('code', ''),
        })
    return issues


def parse_semgrep_results(results: Dict[str, Any]) -> List[Dict[str, str]]:
    """Semgrep結果をパース"""
    issues = []
    for result in results.get('results', []):
        # IPAセクション番号を抽出
        ipa_section = result.get('extra', {}).get('metadata', {}).get('ipa_section', '')

        issues.append({
            'severity': result.get('extra', {}).get('severity', 'WARNING').upper(),
            'rule': result.get('check_id', 'Unknown').split('.')[-1],
            'file': result.get('path', 'Unknown'),
            'line': result.get('start', {}).get('line', '?'),
            'message': result.get('extra', {}).get('message', 'No description'),
            'ipa_section': ipa_section,
        })
    return issues


def severity_emoji(severity: str) -> str:
    """重大度に応じた絵文字を返す"""
    severity_upper = severity.upper()
    if severity_upper in ['CRITICAL', 'HIGH', 'ERROR']:
        return '🔴'
    elif severity_upper in ['MEDIUM', 'WARNING']:
        return '🟡'
    else:
        return '🟢'


def generate_markdown_report(
    bandit_issues: List[Dict],
    semgrep_python_issues: List[Dict],
    semgrep_typescript_issues: List[Dict],
) -> str:
    """Markdown形式のレポートを生成"""

    # 問題の総数をカウント
    total_issues = len(bandit_issues) + len(semgrep_python_issues) + len(semgrep_typescript_issues)

    # 重大度別にカウント
    critical_count = sum(
        1 for issue in (bandit_issues + semgrep_python_issues + semgrep_typescript_issues)
        if issue.get('severity', '').upper() in ['CRITICAL', 'HIGH', 'ERROR']
    )

    # ヘッダー
    if total_issues == 0:
        status_emoji = '✅'
        status_text = 'すべてのセキュリティチェックに合格しました'
    elif critical_count > 0:
        status_emoji = '🔴'
        status_text = f'{critical_count}件の重大な問題が検出されました'
    else:
        status_emoji = '🟡'
        status_text = f'{total_issues}件の警告が検出されました'

    markdown = f"""## 🔒 Security Check Results

{status_emoji} **{status_text}**

---

"""

    # Python (Bandit + Semgrep)
    python_total = len(bandit_issues) + len(semgrep_python_issues)

    if python_total > 0:
        markdown += f"""### 🐍 Python Security ({python_total} issues)

#### Bandit Results ({len(bandit_issues)} issues)

"""
        if bandit_issues:
            markdown += "| Severity | Rule | File | Line | Message |\n"
            markdown += "|----------|------|------|------|----------|\n"
            for issue in sorted(bandit_issues, key=lambda x: x['severity'], reverse=True):
                emoji = severity_emoji(issue['severity'])
                markdown += f"| {emoji} {issue['severity']} | {issue['rule']} | `{issue['file']}` | {issue['line']} | {issue['message'][:80]}... |\n"
        else:
            markdown += "✅ No issues found\n"

        markdown += f"\n#### Semgrep (Python) Results ({len(semgrep_python_issues)} issues)\n\n"

        if semgrep_python_issues:
            markdown += "| Severity | IPA | Rule | File | Line | Message |\n"
            markdown += "|----------|-----|------|------|------|----------|\n"
            for issue in sorted(semgrep_python_issues, key=lambda x: x['severity'], reverse=True):
                emoji = severity_emoji(issue['severity'])
                ipa = issue.get('ipa_section', '-')
                markdown += f"| {emoji} {issue['severity']} | {ipa} | {issue['rule']} | `{issue['file']}` | {issue['line']} | {issue['message'][:60]}... |\n"
        else:
            markdown += "✅ No issues found\n"
    else:
        markdown += "### 🐍 Python Security\n\n✅ No issues found\n"

    markdown += "\n---\n\n"

    # TypeScript/JavaScript (Semgrep)
    if semgrep_typescript_issues:
        markdown += f"""### 📘 TypeScript/JavaScript Security ({len(semgrep_typescript_issues)} issues)

| Severity | IPA | Rule | File | Line | Message |
|----------|-----|------|------|------|----------|
"""
        for issue in sorted(semgrep_typescript_issues, key=lambda x: x['severity'], reverse=True):
            emoji = severity_emoji(issue['severity'])
            ipa = issue.get('ipa_section', '-')
            markdown += f"| {emoji} {issue['severity']} | {ipa} | {issue['rule']} | `{issue['file']}` | {issue['line']} | {issue['message'][:60]}... |\n"
    else:
        markdown += "### 📘 TypeScript/JavaScript Security\n\n✅ No issues found\n"

    # フッター
    markdown += """
---

### 📚 References

- 📖 [セキュリティ規約](./templates/nextjs-fastapi/.cursor/rules/security.mdc)
- ✅ [セキュリティチェックリスト](./templates/nextjs-fastapi/docs/security-checklist.md)
- 🔗 [IPA 安全なウェブサイトの作り方](https://www.ipa.go.jp/security/vuln/websecurity/)

### 💡 Next Steps

"""

    if critical_count > 0:
        markdown += """1. 🔴 **重大な問題を優先的に修正してください**
2. セキュリティ規約を参照して適切な対策を実装
3. 修正後、再度セキュリティチェックを実行
"""
    elif total_issues > 0:
        markdown += """1. 警告内容を確認して必要に応じて修正
2. False positiveの場合は `.bandit` や Semgrep設定で除外を検討
3. セキュリティ規約に沿った実装になっているか確認
"""
    else:
        markdown += "✅ セキュリティチェックに合格しました。そのままマージできます。\n"

    return markdown


def main():
    parser = argparse.ArgumentParser(description='Generate PR comment from security check results')
    parser.add_argument('--results-dir', type=Path, required=True, help='Results directory')
    parser.add_argument('--output', type=Path, required=True, help='Output markdown file')
    args = parser.parse_args()

    # 結果ファイルを読み込む
    bandit_results = load_json_results(
        args.results_dir / 'python-security-results' / 'bandit-results.json'
    )
    semgrep_python_results = load_json_results(
        args.results_dir / 'python-security-results' / 'semgrep-python-results.json'
    )
    semgrep_typescript_results = load_json_results(
        args.results_dir / 'typescript-security-results' / 'semgrep-typescript-results.json'
    )

    # 結果をパース
    bandit_issues = parse_bandit_results(bandit_results)
    semgrep_python_issues = parse_semgrep_results(semgrep_python_results)
    semgrep_typescript_issues = parse_semgrep_results(semgrep_typescript_results)

    # Markdownレポートを生成
    markdown = generate_markdown_report(
        bandit_issues,
        semgrep_python_issues,
        semgrep_typescript_issues,
    )

    # ファイルに出力
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"✅ PR comment generated: {args.output}")


if __name__ == '__main__':
    main()
