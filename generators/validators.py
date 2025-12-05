"""
Configuration Validators

Validates configuration values and provides helpful error messages.
"""

import re
from typing import Dict, List, Tuple
from urllib.parse import urlparse


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class ConfigValidator:
    """Validates configuration values."""

    def __init__(self, variables: Dict[str, str]):
        """
        Initialize ConfigValidator.

        Args:
            variables: Dictionary mapping variable names to values
        """
        self.variables = variables
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """
        Validate all configuration values.

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        # Required fields
        self._validate_required_fields()

        # Project name format
        self._validate_project_name()

        # URL format
        self._validate_repository_url()

        # Database configuration
        self._validate_database_config()

        # Infrastructure platform
        self._validate_infrastructure()

        # Test coverage target
        self._validate_test_coverage()

        # Check for empty values
        self._check_empty_values()

        return len(self.errors) == 0, self.errors, self.warnings

    def _validate_required_fields(self):
        """Validate that required fields are present."""
        required_fields = [
            'PROJECT_NAME',
            'PROJECT_DESCRIPTION',
            'DATABASE_TYPE',
            'INFRASTRUCTURE_PLATFORM'
        ]

        for field in required_fields:
            if field not in self.variables or not self.variables[field]:
                self.errors.append(f"Required field '{field}' is missing or empty")

    def _validate_project_name(self):
        """Validate project name format."""
        project_name = self.variables.get('PROJECT_NAME', '')

        if not project_name:
            return

        # Check for invalid characters
        if not re.match(r'^[a-z0-9-_]+$', project_name):
            self.errors.append(
                f"PROJECT_NAME '{project_name}' contains invalid characters. "
                "Use lowercase letters, numbers, hyphens, and underscores only."
            )

        # Recommend kebab-case
        if '_' in project_name and '-' not in project_name:
            self.warnings.append(
                f"PROJECT_NAME '{project_name}' uses snake_case. "
                "kebab-case is recommended for project names (e.g., my-awesome-project)"
            )

        # Check length
        if len(project_name) < 3:
            self.warnings.append(f"PROJECT_NAME '{project_name}' is very short. Consider a more descriptive name.")

        if len(project_name) > 50:
            self.warnings.append(f"PROJECT_NAME '{project_name}' is very long. Consider a shorter name.")

    def _validate_repository_url(self):
        """Validate repository URL format."""
        repo_url = self.variables.get('REPOSITORY_URL', '')

        if not repo_url or repo_url.startswith('{{'):
            # Allow placeholder or empty
            return

        try:
            parsed = urlparse(repo_url)

            # Check if URL is valid
            if not parsed.scheme or not parsed.netloc:
                self.errors.append(
                    f"REPOSITORY_URL '{repo_url}' is not a valid URL. "
                    "Expected format: https://github.com/org/repo"
                )

            # Check if it's a common git hosting service
            valid_hosts = ['github.com', 'gitlab.com', 'bitbucket.org']
            if parsed.netloc not in valid_hosts:
                self.warnings.append(
                    f"REPOSITORY_URL host '{parsed.netloc}' is not a common git hosting service. "
                    f"Common hosts: {', '.join(valid_hosts)}"
                )

        except Exception as e:
            self.errors.append(f"REPOSITORY_URL validation failed: {e}")

    def _validate_database_config(self):
        """Validate database configuration."""
        db_type = self.variables.get('DATABASE_TYPE', '')

        if not db_type:
            return

        # Check valid database types
        valid_db_types = ['PostgreSQL', 'MySQL', 'SQLite']
        if db_type not in valid_db_types:
            self.warnings.append(
                f"DATABASE_TYPE '{db_type}' is not a common type. "
                f"Common types: {', '.join(valid_db_types)}"
            )

        # Validate port number
        db_port = self.variables.get('DATABASE_PORT', '')
        if db_port and not db_port.startswith('{{'):
            try:
                port_num = int(db_port)
                if port_num < 1 or port_num > 65535:
                    self.errors.append(f"DATABASE_PORT '{db_port}' is out of valid range (1-65535)")

                # Check common ports
                common_ports = {
                    'PostgreSQL': 5432,
                    'MySQL': 3306,
                    'SQLite': None
                }
                expected_port = common_ports.get(db_type)
                if expected_port and port_num != expected_port:
                    self.warnings.append(
                        f"DATABASE_PORT {port_num} is unusual for {db_type}. "
                        f"Common port: {expected_port}"
                    )

            except ValueError:
                self.errors.append(f"DATABASE_PORT '{db_port}' is not a valid number")

        # Validate database URL format
        db_url = self.variables.get('DATABASE_URL_EXAMPLE', '')
        if db_url and not db_url.startswith('{{'):
            if not re.match(r'^[a-z]+\+[a-z]+://', db_url):
                self.warnings.append(
                    f"DATABASE_URL_EXAMPLE '{db_url}' may not be in correct format. "
                    "Expected format: driver+async_driver://user:password@host:port/database"
                )

    def _validate_infrastructure(self):
        """Validate infrastructure platform."""
        platform = self.variables.get('INFRASTRUCTURE_PLATFORM', '')

        if not platform or platform.startswith('{{'):
            return

        # Check valid platforms
        valid_platforms = ['AWS', 'GCP', 'Azure', 'On-Premise', 'Docker', 'Kubernetes']
        if platform not in valid_platforms:
            self.warnings.append(
                f"INFRASTRUCTURE_PLATFORM '{platform}' is not common. "
                f"Common platforms: {', '.join(valid_platforms)}"
            )

    def _validate_test_coverage(self):
        """Validate test coverage target."""
        coverage = self.variables.get('TEST_COVERAGE_TARGET', '')

        if not coverage or coverage.startswith('{{'):
            return

        try:
            coverage_num = int(coverage)

            if coverage_num < 0 or coverage_num > 100:
                self.errors.append(f"TEST_COVERAGE_TARGET '{coverage}' must be between 0 and 100")

            if coverage_num < 60:
                self.warnings.append(
                    f"TEST_COVERAGE_TARGET {coverage_num}% is quite low. "
                    "Industry standard is 70-80%"
                )

            if coverage_num > 95:
                self.warnings.append(
                    f"TEST_COVERAGE_TARGET {coverage_num}% is very high. "
                    "This may be difficult to achieve and maintain"
                )

        except ValueError:
            self.errors.append(f"TEST_COVERAGE_TARGET '{coverage}' is not a valid number")

    def _check_empty_values(self):
        """Check for empty or placeholder values."""
        important_fields = [
            'PROJECT_NAME',
            'PROJECT_DESCRIPTION',
            'ORGANIZATION_NAME',
            'PM_NAME',
            'TECH_LEAD_NAME'
        ]

        for field in important_fields:
            value = self.variables.get(field, '')

            # Check if value is placeholder
            if value.startswith('{{') and value.endswith('}}'):
                self.warnings.append(f"{field} is still a placeholder: {value}")

            # Check if value is empty
            if not value or value.strip() == '':
                self.warnings.append(f"{field} is empty. Consider providing a value")

        # Check FEATURES_LIST specifically
        features_list = self.variables.get('FEATURES_LIST', '')
        if not features_list or features_list.strip() == '':
            self.warnings.append(
                "⚠️ FEATURES_LIST is empty. Please update the 'features' section in template-config.yaml "
                "with your project's actual features"
            )


def validate_config(variables: Dict[str, str]) -> Tuple[bool, List[str], List[str]]:
    """
    Convenience function to validate configuration.

    Args:
        variables: Dictionary mapping variable names to values

    Returns:
        Tuple of (is_valid, errors, warnings)
    """
    validator = ConfigValidator(variables)
    return validator.validate_all()


if __name__ == '__main__':
    # Test the validator
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python validators.py <variables-json>")
        print("\nExample:")
        print('  python validators.py \'{"PROJECT_NAME":"my-app","DATABASE_TYPE":"PostgreSQL"}\'')
        sys.exit(1)

    variables_json = sys.argv[1]

    try:
        variables = json.loads(variables_json)
        validator = ConfigValidator(variables)
        is_valid, errors, warnings = validator.validate_all()

        print("=== Validation Results ===")
        print(f"Valid: {is_valid}\n")

        if errors:
            print("Errors:")
            for error in errors:
                print(f"  ❌ {error}")

        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"  ⚠️  {warning}")

        if not errors and not warnings:
            print("✓ All validations passed")

        sys.exit(0 if is_valid else 1)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
