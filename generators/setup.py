#!/usr/bin/env python3
"""
Template Setup Script

Generates a new project from template by replacing variables with configured values.

Usage:
    python setup.py --config path/to/template-config.yaml --output ../my-new-project
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from config_loader import ConfigLoader
from template_processor import TemplateProcessor
from validators import ConfigValidator
from security_integrator import SecurityIntegrator


class ProjectGenerator:
    """Generates new project from template."""

    def __init__(self, config_path: str, template_name: str = "nextjs-fastapi"):
        """
        Initialize ProjectGenerator.

        Args:
            config_path: Path to template-config.yaml
            template_name: Name of template to use (default: nextjs-fastapi)
        """
        self.config_path = Path(config_path)
        self.template_name = template_name

        # Determine paths
        self.script_dir = Path(__file__).parent
        self.repo_root = self.script_dir.parent
        self.template_dir = self.repo_root / "templates" / template_name

        # Initialize components
        self.loader: Optional[ConfigLoader] = None
        self.processor: Optional[TemplateProcessor] = None
        self.validator: Optional[ConfigValidator] = None

    def generate(self, output_dir: str, validate: bool = True, force: bool = False) -> bool:
        """
        Generate project from template.

        Args:
            output_dir: Path to output directory
            validate: Whether to validate configuration (default: True)
            force: Whether to overwrite existing output directory (default: False)

        Returns:
            True if generation successful, False otherwise
        """
        output_path = Path(output_dir)

        # Check if template exists
        if not self.template_dir.exists():
            print(f"❌ Template not found: {self.template_dir}")
            print(f"\nAvailable templates:")
            templates_dir = self.repo_root / "templates"
            if templates_dir.exists():
                for tmpl in templates_dir.iterdir():
                    if tmpl.is_dir():
                        print(f"  - {tmpl.name}")
            return False

        # Check if output directory exists
        if output_path.exists() and not force:
            print(f"❌ Output directory already exists: {output_path}")
            print("Use --force to overwrite")
            return False

        print(f"📋 Loading configuration from: {self.config_path}")

        # Load configuration
        try:
            self.loader = ConfigLoader(str(self.config_path))
            self.loader.load()
            variables = self.loader.get_variables()
        except Exception as e:
            print(f"❌ Failed to load configuration: {e}")
            return False

        print(f"✓ Loaded {len(variables)} variables")

        # Validate configuration
        if validate:
            print(f"\n🔍 Validating configuration...")
            self.validator = ConfigValidator(variables)
            is_valid, errors, warnings = self.validator.validate_all()

            if warnings:
                print(f"\n⚠️  Warnings:")
                for warning in warnings:
                    print(f"  - {warning}")

            if errors:
                print(f"\n❌ Validation errors:")
                for error in errors:
                    print(f"  - {error}")
                print("\nFix these errors and try again, or use --no-validate to skip validation")
                return False

            print(f"✓ Configuration is valid")

        # Display configuration summary
        self._print_summary(variables)

        # Process template
        print(f"\n🔨 Processing template: {self.template_name}")
        print(f"   Source: {self.template_dir}")
        print(f"   Output: {output_path}")

        try:
            self.processor = TemplateProcessor(
                str(self.template_dir),
                str(output_path),
                variables
            )
            result = self.processor.process_all()

            print(f"\n✓ Processed {len(result['processed'])} files")
            if result['skipped']:
                print(f"  Skipped {len(result['skipped'])} files")

        except Exception as e:
            print(f"\n❌ Failed to process template: {e}")
            import traceback
            traceback.print_exc()
            return False

        # Validate output
        print(f"\n🔍 Validating output...")
        unreplaced = self.processor.validate_output()

        if unreplaced:
            print(f"\n⚠️  Found unreplaced variables:")
            for file_path, vars_list in unreplaced.items():
                rel_path = Path(file_path).relative_to(output_path)
                print(f"  {rel_path}: {', '.join(vars_list)}")
            print("\nThese variables may need manual replacement")
        else:
            print(f"✓ All variables replaced successfully")

        # Integrate security template
        security_integrator = SecurityIntegrator(
            self.repo_root,
            self.template_name,
            output_path
        )
        security_integrator.integrate()

        # Success message
        print(f"\n{'=' * 60}")
        print(f"🎉 Project generated successfully!")
        print(f"{'=' * 60}")
        print(f"\nNext steps:")
        print(f"1. cd {output_path}")
        print(f"2. Review and customize CLAUDE.md and other files")
        print(f"3. Initialize git repository: git init")
        print(f"4. Set up development environment")
        print(f"\nFor setup instructions, see:")
        print(f"  {output_path / 'README.md'}")

        return True

    def _print_summary(self, variables: dict):
        """Print configuration summary."""
        print(f"\n{'=' * 60}")
        print(f"Project Configuration Summary")
        print(f"{'=' * 60}")
        print(f"Project Name:     {variables.get('PROJECT_NAME', 'N/A')}")
        print(f"Description:      {variables.get('PROJECT_DESCRIPTION', 'N/A')}")
        print(f"Database:         {variables.get('DATABASE_TYPE', 'N/A')} {variables.get('DATABASE_VERSION', '')}")
        print(f"Infrastructure:   {variables.get('INFRASTRUCTURE_PLATFORM', 'N/A')}")
        print(f"Organization:     {variables.get('ORGANIZATION_NAME', 'N/A')}")
        print(f"Tech Lead:        {variables.get('TECH_LEAD_NAME', 'N/A')}")
        print(f"PM:               {variables.get('PM_NAME', 'N/A')}")
        print(f"Coverage Target:  {variables.get('TEST_COVERAGE_TARGET', 'N/A')}%")
        print(f"{'=' * 60}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate a new project from template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate project with configuration file
  python setup.py --config template-config.yaml --output ../my-new-project

  # Use different template
  python setup.py --config config.yaml --output ../my-app --template flutter-fastapi

  # Skip validation (not recommended)
  python setup.py --config config.yaml --output ../my-app --no-validate

  # Overwrite existing output directory
  python setup.py --config config.yaml --output ../my-app --force
        """
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to template-config.yaml file"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path to output directory"
    )

    parser.add_argument(
        "--template",
        default="nextjs-fastapi",
        help="Template name to use (default: nextjs-fastapi)"
    )

    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip configuration validation (not recommended)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing output directory"
    )

    args = parser.parse_args()

    # Generate project
    generator = ProjectGenerator(args.config, args.template)
    success = generator.generate(
        args.output,
        validate=not args.no_validate,
        force=args.force
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
