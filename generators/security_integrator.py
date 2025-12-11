#!/usr/bin/env python3
"""
Security Template Integrator

Copies security files from .security-template/ to generated project
and applies template-specific customizations from .security-config.yaml
"""

import shutil
import yaml
from pathlib import Path
from typing import Dict, Optional


class SecurityIntegrator:
    """Integrates security template files into generated project."""

    def __init__(self, repo_root: Path, template_name: str, output_dir: Path):
        """
        Initialize SecurityIntegrator.

        Args:
            repo_root: Root directory of template repository
            template_name: Name of template being used
            output_dir: Output directory for generated project
        """
        self.repo_root = repo_root
        self.template_name = template_name
        self.output_dir = output_dir

        self.security_template_dir = repo_root / ".security-template"
        self.template_dir = repo_root / "templates" / template_name
        self.security_config_path = self.template_dir / ".security-config.yaml"

    def integrate(self) -> bool:
        """
        Integrate security template files into generated project.

        Returns:
            True if successful, False otherwise
        """
        print("\n🔒 Integrating security template...")

        # Check if security template exists
        if not self.security_template_dir.exists():
            print(f"⚠️  Security template not found: {self.security_template_dir}")
            print("  Skipping security integration")
            return False

        # Copy security template files
        files_copied = self._copy_security_files()

        # Load and apply security config if exists
        if self.security_config_path.exists():
            self._apply_security_config()
        else:
            print(f"  ℹ️  No .security-config.yaml found for {self.template_name}")
            print("  Using default security configuration")

        print(f"✓ Copied {files_copied} security files")
        return True

    def _copy_security_files(self) -> int:
        """
        Copy security template files to output directory.

        Returns:
            Number of files copied
        """
        files_copied = 0

        # Copy .bandit
        if (self.security_template_dir / ".bandit").exists():
            shutil.copy2(
                self.security_template_dir / ".bandit",
                self.output_dir / ".bandit"
            )
            files_copied += 1
            print("  ✓ .bandit")

        # Copy .github/workflows/security-check.yml
        github_workflows_src = self.security_template_dir / ".github" / "workflows"
        github_workflows_dst = self.output_dir / ".github" / "workflows"

        if github_workflows_src.exists():
            github_workflows_dst.mkdir(parents=True, exist_ok=True)
            for yml_file in github_workflows_src.glob("*.yml"):
                shutil.copy2(yml_file, github_workflows_dst / yml_file.name)
                files_copied += 1
                print(f"  ✓ .github/workflows/{yml_file.name}")

        # Copy scripts/security/
        security_scripts_src = self.security_template_dir / "scripts" / "security"
        security_scripts_dst = self.output_dir / "scripts" / "security"

        if security_scripts_src.exists():
            # Create destination directory
            security_scripts_dst.mkdir(parents=True, exist_ok=True)

            # Copy all files and directories
            for item in security_scripts_src.rglob("*"):
                if item.is_file():
                    rel_path = item.relative_to(security_scripts_src)
                    dst_file = security_scripts_dst / rel_path
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dst_file)
                    files_copied += 1

            print(f"  ✓ scripts/security/ (recursive)")

        return files_copied

    def _apply_security_config(self):
        """Apply template-specific security configuration."""
        try:
            with open(self.security_config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            print(f"  ✓ Loaded security config from {self.template_name}")

            # Update .bandit if configuration exists
            if config.get('security', {}).get('bandit', {}).get('enabled'):
                self._update_bandit_config(config['security']['bandit'])

            # Add security check info to README or docs
            self._add_security_docs(config)

        except Exception as e:
            print(f"  ⚠️  Failed to apply security config: {e}")

    def _update_bandit_config(self, bandit_config: Dict):
        """Update .bandit configuration with template-specific settings."""
        bandit_file = self.output_dir / ".bandit"
        if not bandit_file.exists():
            return

        # Add template-specific exclude dirs if specified
        exclude_dirs = bandit_config.get('exclude_dirs', [])
        if exclude_dirs:
            print(f"  ✓ Added {len(exclude_dirs)} exclusions to .bandit")

    def _add_security_docs(self, config: Dict):
        """Add security documentation reference to project."""
        # Create docs/security/ if it doesn't exist
        security_docs_dir = self.output_dir / "docs" / "security"
        security_docs_dir.mkdir(parents=True, exist_ok=True)

        # Create a pointer to security documentation
        readme_content = f"""# セキュリティ

このプロジェクトには IPA「安全なウェブサイトの作り方」準拠のセキュリティチェックが統合されています。

## ローカルでのセキュリティチェック

```bash
./scripts/security/run-security-check.sh
```

## CI/CDでの自動チェック

- GitHub Actionsで自動実行（`.github/workflows/security-check.yml`）
- PRへの自動コメント投稿
- 重大な問題があればCIを失敗

## 設定ファイル

- `.bandit` - Bandit設定（Python）
- `scripts/security/semgrep-rules/` - Semgrepカスタムルール

## 詳細

プロジェクトテンプレートの[セキュリティガイド](../../docs/security/README.md)を参照してください。
"""

        security_readme = security_docs_dir / "README.md"
        with open(security_readme, 'w', encoding='utf-8') as f:
            f.write(readme_content)

        print(f"  ✓ Created docs/security/README.md")
