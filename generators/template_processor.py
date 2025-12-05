"""
Template Processor

Processes template files by replacing variables with configured values.
"""

import re
import shutil
from pathlib import Path
from typing import Dict, List, Set


class TemplateProcessor:
    """Processes template files and replaces variables."""

    def __init__(self, template_dir: str, output_dir: str, variables: Dict[str, str]):
        """
        Initialize TemplateProcessor.

        Args:
            template_dir: Path to template directory
            output_dir: Path to output directory
            variables: Dictionary mapping variable names to values
        """
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        self.variables = variables
        self.processed_files: List[Path] = []
        self.skipped_files: List[Path] = []

    def process_all(self, exclude_patterns: List[str] = None) -> Dict[str, List[Path]]:
        """
        Process all template files in template directory.

        Args:
            exclude_patterns: List of glob patterns to exclude (e.g., ['*.pyc', '__pycache__'])

        Returns:
            Dictionary with 'processed' and 'skipped' file lists
        """
        if exclude_patterns is None:
            exclude_patterns = [
                '*.pyc',
                '__pycache__',
                '.DS_Store',
                '*.egg-info',
                '.git',
                'node_modules',
                'venv',
                '.venv',
                'dist',
                'build'
            ]

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Process all files
        for source_path in self.template_dir.rglob('*'):
            # Skip directories
            if source_path.is_dir():
                continue

            # Check exclude patterns
            if self._should_exclude(source_path, exclude_patterns):
                self.skipped_files.append(source_path)
                continue

            # Calculate relative path
            rel_path = source_path.relative_to(self.template_dir)

            # Process file
            self._process_file(source_path, rel_path)

        return {
            'processed': self.processed_files,
            'skipped': self.skipped_files
        }

    def _should_exclude(self, path: Path, exclude_patterns: List[str]) -> bool:
        """Check if path matches any exclude pattern."""
        for pattern in exclude_patterns:
            if path.match(pattern) or any(part.startswith('.') and part != '.github' and part != '.vscode' and part != '.cursor' for part in path.parts):
                return True
        return False

    def _process_file(self, source_path: Path, rel_path: Path):
        """
        Process a single template file.

        Args:
            source_path: Source file path
            rel_path: Relative path from template root
        """
        # Determine output path (remove .template extension if present)
        if source_path.suffix == '.template':
            output_rel_path = rel_path.with_suffix('')
        else:
            output_rel_path = rel_path

        output_path = self.output_dir / output_rel_path

        # Create parent directories
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Check if file is text or binary
        if self._is_text_file(source_path):
            self._process_text_file(source_path, output_path)
        else:
            self._copy_binary_file(source_path, output_path)

        self.processed_files.append(output_path)

    def _is_text_file(self, path: Path) -> bool:
        """
        Determine if file is text (should be processed) or binary (should be copied).

        Args:
            path: File path to check

        Returns:
            True if text file, False if binary
        """
        text_extensions = {
            '.md', '.txt', '.json', '.yaml', '.yml', '.toml',
            '.py', '.js', '.ts', '.jsx', '.tsx', '.css', '.scss',
            '.html', '.xml', '.svg', '.sh', '.bash',
            '.gitignore', '.env', '.example', '.template',
            '.mdc'  # Cursor rules files
        }

        # Check by extension
        if path.suffix in text_extensions:
            return True

        # Check files without extension (like .gitignore, Dockerfile)
        if path.suffix == '' and path.name in ['.gitignore', 'Dockerfile', 'LICENSE', 'README', 'Makefile']:
            return True

        # Try to read as text
        try:
            with open(path, 'r', encoding='utf-8') as f:
                f.read(1024)  # Read first 1KB
            return True
        except (UnicodeDecodeError, PermissionError):
            return False

    def _process_text_file(self, source_path: Path, output_path: Path):
        """
        Process text file by replacing variables.

        Args:
            source_path: Source file path
            output_path: Output file path
        """
        try:
            # Read source file
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace variables
            processed_content = self._replace_variables(content)

            # Write output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)

        except Exception as e:
            print(f"Warning: Failed to process {source_path}: {e}")
            # Fallback to binary copy
            self._copy_binary_file(source_path, output_path)

    def _copy_binary_file(self, source_path: Path, output_path: Path):
        """
        Copy binary file without modification.

        Args:
            source_path: Source file path
            output_path: Output file path
        """
        shutil.copy2(source_path, output_path)

    def _replace_variables(self, content: str) -> str:
        """
        Replace template variables in content.

        Variables are in format: {{VARIABLE_NAME}}

        Args:
            content: File content with template variables

        Returns:
            Content with variables replaced
        """
        # Replace each variable
        for var_name, var_value in self.variables.items():
            pattern = r'\{\{' + re.escape(var_name) + r'\}\}'
            content = re.sub(pattern, var_value, content)

        return content

    def get_unreplaced_variables(self, content: str) -> Set[str]:
        """
        Find variables that haven't been replaced.

        Args:
            content: File content

        Returns:
            Set of unreplaced variable names
        """
        pattern = r'\{\{([A-Z_]+)\}\}'
        matches = re.findall(pattern, content)
        return set(matches)

    def validate_output(self) -> Dict[str, List[str]]:
        """
        Validate output files for unreplaced variables.

        Returns:
            Dictionary mapping file paths to lists of unreplaced variables
        """
        unreplaced = {}

        for file_path in self.processed_files:
            if not file_path.exists() or not file_path.is_file():
                continue

            if not self._is_text_file(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                unreplaced_vars = self.get_unreplaced_variables(content)
                if unreplaced_vars:
                    unreplaced[str(file_path)] = sorted(unreplaced_vars)

            except Exception:
                continue

        return unreplaced


def process_template(template_dir: str, output_dir: str, variables: Dict[str, str],
                     exclude_patterns: List[str] = None) -> Dict[str, List[Path]]:
    """
    Convenience function to process template directory.

    Args:
        template_dir: Path to template directory
        output_dir: Path to output directory
        variables: Dictionary mapping variable names to values
        exclude_patterns: List of glob patterns to exclude

    Returns:
        Dictionary with 'processed' and 'skipped' file lists
    """
    processor = TemplateProcessor(template_dir, output_dir, variables)
    return processor.process_all(exclude_patterns)


if __name__ == '__main__':
    # Test the template processor
    import sys
    import json

    if len(sys.argv) < 4:
        print("Usage: python template_processor.py <template-dir> <output-dir> <variables-json>")
        print("\nExample:")
        print('  python template_processor.py templates/nextjs-fastapi output \'{"PROJECT_NAME":"test"}\'')
        sys.exit(1)

    template_dir = sys.argv[1]
    output_dir = sys.argv[2]
    variables_json = sys.argv[3]

    try:
        variables = json.loads(variables_json)
        processor = TemplateProcessor(template_dir, output_dir, variables)
        result = processor.process_all()

        print(f"\n=== Processing Complete ===")
        print(f"Processed: {len(result['processed'])} files")
        print(f"Skipped: {len(result['skipped'])} files")

        # Validate output
        unreplaced = processor.validate_output()
        if unreplaced:
            print(f"\n=== Warning: Unreplaced Variables ===")
            for file_path, vars_list in unreplaced.items():
                print(f"{file_path}: {', '.join(vars_list)}")
        else:
            print(f"\n✓ All variables replaced successfully")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
