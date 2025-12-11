#!/usr/bin/env python3
"""
重大な問題のチェックスクリプト
セキュリティチェック結果から重大度の高い問題をカウント
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Any


def load_json_results(file_path: Path) -> Dict[str, Any]:
    """JSON結果ファイルを読み込む"""
    if not file_path.exists():
        return {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def count_critical_bandit(results: Dict[str, Any]) -> int:
    """Banditの重大な問題をカウント"""
    count = 0
    for result in results.get('results', []):
        severity = result.get('issue_severity', '').upper()
        if severity in ['HIGH', 'CRITICAL']:
            count += 1
    return count


def count_critical_semgrep(results: Dict[str, Any]) -> int:
    """Semgrepの重大な問題をカウント"""
    count = 0
    for result in results.get('results', []):
        severity = result.get('extra', {}).get('severity', '').upper()
        if severity in ['ERROR', 'HIGH', 'CRITICAL']:
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description='Count critical security issues')
    parser.add_argument('--results-dir', type=Path, required=True, help='Results directory')
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

    # 重大な問題をカウント
    critical_count = 0
    critical_count += count_critical_bandit(bandit_results)
    critical_count += count_critical_semgrep(semgrep_python_results)
    critical_count += count_critical_semgrep(semgrep_typescript_results)

    # 結果を出力
    print(critical_count)

    # 重大な問題がある場合は終了コード1
    if critical_count > 0:
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
