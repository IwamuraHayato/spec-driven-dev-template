"""
Template Configuration Loader

Loads and parses template-config.yaml file to extract project configuration.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigLoader:
    """Loads template configuration from YAML file."""

    def __init__(self, config_path: str):
        """
        Initialize ConfigLoader.

        Args:
            config_path: Path to template-config.yaml
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}

    def load(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.

        Returns:
            Dictionary containing configuration values

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        return self.config

    def get_variables(self) -> Dict[str, str]:
        """
        Extract template variables from configuration.

        Returns:
            Dictionary mapping variable names to values
        """
        variables = {}

        # Project info
        project = self.config.get('project', {})
        variables['PROJECT_NAME'] = project.get('name', '')
        variables['PROJECT_DESCRIPTION'] = project.get('description', '')
        variables['REPOSITORY_URL'] = project.get('repository_url', '')

        # Tech stack
        tech_stack = self.config.get('tech_stack', {})

        # Database configuration
        database = tech_stack.get('database', {})
        variables['DATABASE_TYPE'] = database.get('primary', 'PostgreSQL')
        variables['DATABASE_VERSION'] = database.get('version', '14+')
        variables['DATABASE_PORT'] = database.get('port', '5432')
        variables['DATABASE_CLIENT_TOOLS'] = database.get('client_tools', 'psql, pgAdmin, DBeaver')
        variables['DATABASE_URL_EXAMPLE'] = database.get('url_example', 'postgresql+asyncpg://user:password@localhost:5432/dbname')

        # Infrastructure
        infrastructure = tech_stack.get('infrastructure', {})
        variables['INFRASTRUCTURE_PLATFORM'] = infrastructure.get('platform', 'AWS')

        # Team info
        team = self.config.get('team', {})
        variables['ORGANIZATION_NAME'] = team.get('organization', '')
        variables['PM_NAME'] = team.get('project_manager', '')
        variables['TECH_LEAD_NAME'] = team.get('tech_lead', '')

        # Development settings
        development = self.config.get('development', {})
        variables['TEST_COVERAGE_TARGET'] = str(development.get('test_coverage_target', 80))

        # Features list
        features = self.config.get('features', [])
        features_list = '\n'.join([f"- {feature}" for feature in features if not feature.startswith('{{')])
        variables['FEATURES_LIST'] = features_list

        # Target user description (optional)
        variables['TARGET_USER_DESCRIPTION'] = self.config.get('target_user_description', 'エンドユーザー')

        # License (optional)
        variables['LICENSE'] = self.config.get('license', 'MIT')

        return variables

    def get_database_config(self) -> Dict[str, str]:
        """
        Get database-specific configuration helper.

        Returns:
            Dictionary with database type, port, and connection details
        """
        tech_stack = self.config.get('tech_stack', {})
        database = tech_stack.get('database', {})

        db_type = database.get('primary', 'PostgreSQL')

        # Default configurations for each database type
        defaults = {
            'PostgreSQL': {
                'port': '5432',
                'version': '14+',
                'client_tools': 'psql, pgAdmin, DBeaver',
                'url_example': 'postgresql+asyncpg://user:password@localhost:5432/dbname',
                'driver': 'asyncpg',
                'driver_package': 'asyncpg'
            },
            'MySQL': {
                'port': '3306',
                'version': '8.0+',
                'client_tools': 'mysql, MySQL Workbench, DBeaver',
                'url_example': 'mysql+aiomysql://user:password@localhost:3306/dbname',
                'driver': 'aiomysql',
                'driver_package': 'aiomysql'
            }
        }

        default_config = defaults.get(db_type, defaults['PostgreSQL'])

        return {
            'type': db_type,
            'port': database.get('port', default_config['port']),
            'version': database.get('version', default_config['version']),
            'client_tools': database.get('client_tools', default_config['client_tools']),
            'url_example': database.get('url_example', default_config['url_example']),
            'driver': default_config['driver'],
            'driver_package': default_config['driver_package']
        }


def load_config(config_path: str) -> Dict[str, str]:
    """
    Convenience function to load configuration and extract variables.

    Args:
        config_path: Path to template-config.yaml

    Returns:
        Dictionary mapping variable names to values
    """
    loader = ConfigLoader(config_path)
    loader.load()
    return loader.get_variables()


if __name__ == '__main__':
    # Test the config loader
    import sys

    if len(sys.argv) < 2:
        print("Usage: python config_loader.py <path-to-template-config.yaml>")
        sys.exit(1)

    config_path = sys.argv[1]

    try:
        loader = ConfigLoader(config_path)
        loader.load()
        variables = loader.get_variables()

        print("=== Configuration Variables ===")
        for key, value in variables.items():
            print(f"{key}: {value}")

        print("\n=== Database Configuration ===")
        db_config = loader.get_database_config()
        for key, value in db_config.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
