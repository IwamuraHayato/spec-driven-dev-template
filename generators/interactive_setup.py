#!/usr/bin/env python3
"""
Interactive Template Setup

Guides user through configuration and generates project.

Usage:
    python interactive_setup.py
"""

import sys
from pathlib import Path
from typing import Dict

import yaml

from setup import ProjectGenerator


class InteractiveSetup:
    """Interactive project setup wizard."""

    def __init__(self):
        """Initialize InteractiveSetup."""
        self.variables: Dict[str, str] = {}
        self.config: Dict = {}

    def run(self) -> bool:
        """
        Run interactive setup wizard.

        Returns:
            True if successful, False otherwise
        """
        print("=" * 70)
        print("🚀 Spec-Driven Development Template - Interactive Setup")
        print("=" * 70)
        print("\nThis wizard will guide you through setting up a new project.")
        print("Press Enter to use default values shown in [brackets].\n")

        # Project information
        self._setup_project_info()

        # Tech stack
        self._setup_tech_stack()

        # Team information
        self._setup_team_info()

        # Features
        self._setup_features()

        # Development settings
        self._setup_development()

        # Output configuration
        self._setup_output()

        # Summary and confirmation
        if not self._confirm_and_generate():
            print("\n❌ Setup cancelled")
            return False

        return True

    def _setup_project_info(self):
        """Setup project information."""
        print("\n📋 Project Information")
        print("-" * 70)

        self.variables['PROJECT_NAME'] = self._prompt(
            "Project name (lowercase, use hyphens)",
            "my-awesome-project"
        )

        self.variables['PROJECT_DESCRIPTION'] = self._prompt(
            "Project description",
            "A modern web application"
        )

        self.variables['REPOSITORY_URL'] = self._prompt(
            "Repository URL",
            f"https://github.com/your-org/{self.variables['PROJECT_NAME']}"
        )

        self.variables['LICENSE'] = self._prompt(
            "License",
            "MIT",
            choices=["MIT", "Apache 2.0", "Proprietary", "Other"]
        )

    def _setup_tech_stack(self):
        """Setup technology stack."""
        print("\n🔧 Technology Stack")
        print("-" * 70)

        # Database
        db_type = self._prompt(
            "Database type",
            "PostgreSQL",
            choices=["PostgreSQL", "MySQL"]
        )
        self.variables['DATABASE_TYPE'] = db_type

        # Database version
        if db_type == "PostgreSQL":
            self.variables['DATABASE_VERSION'] = self._prompt("PostgreSQL version", "14+")
            self.variables['DATABASE_PORT'] = "5432"
            self.variables['DATABASE_CLIENT_TOOLS'] = "psql, pgAdmin, DBeaver"
            self.variables['DATABASE_URL_EXAMPLE'] = "postgresql+asyncpg://user:password@localhost:5432/dbname"
        else:  # MySQL
            self.variables['DATABASE_VERSION'] = self._prompt("MySQL version", "8.0+")
            self.variables['DATABASE_PORT'] = "3306"
            self.variables['DATABASE_CLIENT_TOOLS'] = "mysql, MySQL Workbench, DBeaver"
            self.variables['DATABASE_URL_EXAMPLE'] = "mysql+aiomysql://user:password@localhost:3306/dbname"

        # Infrastructure
        self.variables['INFRASTRUCTURE_PLATFORM'] = self._prompt(
            "Infrastructure platform",
            "AWS",
            choices=["AWS", "GCP", "Azure", "On-Premise", "Docker"]
        )

    def _setup_team_info(self):
        """Setup team information."""
        print("\n👥 Team Information")
        print("-" * 70)

        self.variables['ORGANIZATION_NAME'] = self._prompt(
            "Organization name",
            "Your Company"
        )

        self.variables['PM_NAME'] = self._prompt(
            "Project Manager name",
            "山田太郎"
        )

        self.variables['TECH_LEAD_NAME'] = self._prompt(
            "Technical Lead name",
            "鈴木花子"
        )

    def _setup_features(self):
        """Setup project features."""
        print("\n✨ Main Features")
        print("-" * 70)
        print("Enter main features (one per line, empty line to finish):")

        features = []
        index = 1
        while True:
            feature = input(f"  {index}. ").strip()
            if not feature:
                break
            features.append(feature)
            index += 1

        if not features:
            features = ["ユーザー認証機能", "データダッシュボード", "レポート生成機能"]
            print(f"Using default features: {', '.join(features)}")

        self.variables['FEATURES_LIST'] = '\n'.join([f"- {f}" for f in features])

        # Store features for YAML config
        self.config['features'] = features

    def _setup_development(self):
        """Setup development settings."""
        print("\n🧪 Development Settings")
        print("-" * 70)

        coverage = self._prompt(
            "Test coverage target (%)",
            "80"
        )

        try:
            coverage_num = int(coverage)
            if coverage_num < 0 or coverage_num > 100:
                print("⚠️  Coverage must be 0-100, using 80")
                coverage = "80"
        except ValueError:
            print("⚠️  Invalid number, using 80")
            coverage = "80"

        self.variables['TEST_COVERAGE_TARGET'] = coverage

        self.variables['TARGET_USER_DESCRIPTION'] = self._prompt(
            "Target user description",
            "エンドユーザー向けサービス利用者"
        )

    def _setup_output(self):
        """Setup output configuration."""
        print("\n📁 Output Configuration")
        print("-" * 70)

        default_output = f"../{self.variables['PROJECT_NAME']}"
        self.output_dir = self._prompt(
            "Output directory",
            default_output
        )

        self.template_name = self._prompt(
            "Template name",
            "nextjs-fastapi",
            choices=["nextjs-fastapi"]
        )

    def _confirm_and_generate(self) -> bool:
        """Show summary and confirm generation."""
        print("\n" + "=" * 70)
        print("📝 Configuration Summary")
        print("=" * 70)
        print(f"Project Name:     {self.variables['PROJECT_NAME']}")
        print(f"Description:      {self.variables['PROJECT_DESCRIPTION']}")
        print(f"Database:         {self.variables['DATABASE_TYPE']} {self.variables['DATABASE_VERSION']}")
        print(f"Infrastructure:   {self.variables['INFRASTRUCTURE_PLATFORM']}")
        print(f"Organization:     {self.variables['ORGANIZATION_NAME']}")
        print(f"PM:               {self.variables['PM_NAME']}")
        print(f"Tech Lead:        {self.variables['TECH_LEAD_NAME']}")
        print(f"Coverage Target:  {self.variables['TEST_COVERAGE_TARGET']}%")
        print(f"Output Directory: {self.output_dir}")
        print(f"Template:         {self.template_name}")
        print("=" * 70)

        confirm = self._prompt(
            "\nGenerate project with this configuration? (yes/no)",
            "yes",
            choices=["yes", "no"]
        )

        if confirm.lower() != "yes":
            return False

        # Save configuration to temporary file
        temp_config_path = self._save_temp_config()

        print(f"\n💾 Configuration saved to: {temp_config_path}")

        # Generate project
        print("\n🔨 Generating project...\n")

        generator = ProjectGenerator(str(temp_config_path), self.template_name)
        success = generator.generate(self.output_dir, validate=True, force=False)

        return success

    def _save_temp_config(self) -> Path:
        """Save configuration to temporary YAML file."""
        script_dir = Path(__file__).parent
        temp_config_path = script_dir / "temp-config.yaml"

        # Build full config structure
        config = {
            'project': {
                'name': self.variables['PROJECT_NAME'],
                'description': self.variables['PROJECT_DESCRIPTION'],
                'repository_url': self.variables['REPOSITORY_URL']
            },
            'tech_stack': {
                'frontend': {
                    'framework': 'Next.js',
                    'version': '15+',
                    'language': 'TypeScript',
                    'styling': 'Tailwind CSS',
                    'state_management': 'React Context / Zustand',
                    'package_manager': 'npm'
                },
                'backend': {
                    'framework': 'FastAPI',
                    'version': '0.104+',
                    'language': 'Python',
                    'python_version': '3.12+',
                    'orm': 'SQLAlchemy',
                    'migration': 'Alembic'
                },
                'database': {
                    'primary': self.variables['DATABASE_TYPE'],
                    'version': self.variables['DATABASE_VERSION'],
                    'port': self.variables['DATABASE_PORT'],
                    'client_tools': self.variables['DATABASE_CLIENT_TOOLS'],
                    'url_example': self.variables['DATABASE_URL_EXAMPLE']
                },
                'infrastructure': {
                    'platform': self.variables['INFRASTRUCTURE_PLATFORM'],
                    'containerization': 'Docker'
                }
            },
            'features': self.config.get('features', []),
            'team': {
                'organization': self.variables['ORGANIZATION_NAME'],
                'project_manager': self.variables['PM_NAME'],
                'tech_lead': self.variables['TECH_LEAD_NAME']
            },
            'development': {
                'branch_strategy': 'git-flow',
                'main_branch': 'main',
                'develop_branch': 'develop',
                'test_coverage_target': int(self.variables['TEST_COVERAGE_TARGET'])
            },
            'code_quality': {
                'frontend': {
                    'linter': 'ESLint',
                    'formatter': 'Prettier'
                },
                'backend': {
                    'linter': 'Ruff',
                    'formatter': 'Ruff',
                    'type_checker': 'MyPy'
                }
            },
            'ci_cd': {
                'platform': 'GitHub Actions',
                'auto_review': True,
                'auto_deploy': False
            },
            'target_user_description': self.variables['TARGET_USER_DESCRIPTION'],
            'license': self.variables['LICENSE']
        }

        # Write YAML
        with open(temp_config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        return temp_config_path

    def _prompt(self, question: str, default: str = "", choices: list = None) -> str:
        """
        Prompt user for input.

        Args:
            question: Question to ask
            default: Default value
            choices: List of valid choices (optional)

        Returns:
            User input or default value
        """
        if choices:
            choices_str = " (" + "/".join(choices) + ")"
        else:
            choices_str = ""

        if default:
            prompt = f"{question}{choices_str} [{default}]: "
        else:
            prompt = f"{question}{choices_str}: "

        while True:
            value = input(prompt).strip()

            if not value and default:
                return default

            if not value:
                print("⚠️  This field is required")
                continue

            if choices and value not in choices:
                print(f"⚠️  Please choose from: {', '.join(choices)}")
                continue

            return value


def main():
    """Main entry point."""
    try:
        setup = InteractiveSetup()
        success = setup.run()
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
