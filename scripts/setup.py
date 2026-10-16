"""Template setup script — replaces placeholder names with your project name."""

import re
import sys
from pathlib import Path

# Files to skip during replacement
SKIP_DIRS = {".git", ".venv", "__pycache__", ".direnv", "node_modules"}
SKIP_FILES = {"setup.py"}

# Extensions to process
TEXT_EXTENSIONS = {".py", ".toml", ".md", ".yml", ".yaml", ".json"}

ROOT = Path(__file__).resolve().parent.parent


def find_text_files(root: Path) -> list[Path]:
    """Find all text files eligible for replacement."""
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(skip in path.parts for skip in SKIP_DIRS):
            continue
        if path.name in SKIP_FILES:
            continue
        if path.is_file() and path.suffix in TEXT_EXTENSIONS:
            files.append(path)
    return files


def replace_in_file(path: Path, old: str, new: str) -> bool:
    """Replace all occurrences of old with new in a file. Returns True if changed."""
    content = path.read_text()
    updated = content.replace(old, new)
    if content != updated:
        path.write_text(updated)
        return True
    return False


def rename_source_dirs(root: Path, old_name: str, new_name: str) -> list[str]:
    """Rename src/<old_name>/ directories to src/<new_name>/."""
    renamed: list[str] = []
    for src_dir in root.rglob("src"):
        if not src_dir.is_dir():
            continue
        old_pkg = src_dir / old_name
        if old_pkg.is_dir():
            new_pkg = src_dir / new_name
            old_pkg.rename(new_pkg)
            renamed.append(f"  {old_pkg.relative_to(root)} -> {new_pkg.relative_to(root)}")
    return renamed


def main() -> None:
    project_name = input("Project name (e.g. myproject): ").strip()
    if not project_name:
        print("Error: project name required")
        sys.exit(1)

    if not re.match(r"^[a-z][a-z0-9_-]*$", project_name):
        print("Error: project name must be lowercase alphanumeric with hyphens/underscores")
        sys.exit(1)

    # Derive package-safe name (underscores for Python imports)
    pkg_name = project_name.replace("-", "_")

    print(f"\nProject name: {project_name}")
    print(f"Package name: {pkg_name}")
    confirm = input("Continue? [y/N] ").strip().lower()
    if confirm != "y":
        print("Aborted.")
        sys.exit(0)

    # Replace in file contents
    files = find_text_files(ROOT)
    changed = 0
    for path in files:
        # Replace the project-level name
        if replace_in_file(path, "python-template", project_name):
            changed += 1
        # Replace the root pyproject name reference
        replace_in_file(path, "python_template", pkg_name)

    print(f"\nReplaced references in {changed} files")

    # Rename source directories is left to the user since core/utils
    # are generic names that should be renamed per-project needs

    print("\nDone! Next steps:")
    print("  1. Rename packages/core and packages/utils to match your project")
    print("  2. Update package names in their pyproject.toml files")
    print("  3. Update imports in source files")
    print("  4. Run: uv sync")
    print("  5. Run: uv run pytest")
    print("  6. Delete SETUP.md")


if __name__ == "__main__":
    main()
