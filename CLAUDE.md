# python-template

Python monorepo template using uv workspaces with the Astral toolchain (uv, ruff, ty).

## Quick Reference

```bash
mise install --locked    # install pinned tools (uv, ruff, ty, lefthook, jq, ripgrep)
uv sync                  # install all workspace dependencies
uv run pytest            # run all tests
uv run ruff check .      # lint
uv run ruff format .     # format
uv run ruff format --check .  # check format without writing
uv run ty check          # type check
uv run example           # run the example app
```

## Project Layout

```
apps/           # applications (executables, services)
  example/      # example app — imports from packages/utils
packages/       # libraries (shared code)
  core/         # core library — exports VERSION
  utils/        # utility library — depends on core
scripts/        # development scripts
  setup.py      # template scope replacement
```

## Workspace Structure

Each workspace member has its own `pyproject.toml` with:
- `src/<name>/` layout (PEP 517)
- `tests/` directory colocated with the package
- `hatchling` as build backend

Dependencies between workspace members use `[tool.uv.sources]` with `workspace = true`.

## Toolchain

| Tool | Purpose |
|------|---------|
| uv | Package manager, workspaces, venv, Python version management |
| ruff | Linter and formatter (replaces flake8, black, isort) |
| ty | Type checker (Astral, Rust-based) |
| pytest | Test runner |
| lefthook | Git hooks (pre-commit, pre-push) |
| mise | Pinned, checksum-locked dev tools (`mise.toml`, `mise.lock`) |

## Conventions

- Type hints on all function signatures
- `frozen=True` dataclasses for data models
- Raise descriptive exceptions for unhandled cases
- Tests colocated in `tests/` within each package
- `ruff.toml` at root applies to all workspace members
- Line length: 120
- Target: Python 3.13+

## Adding a Package

1. Create `packages/<name>/pyproject.toml` with hatchling build backend
2. Create `packages/<name>/src/<name>/__init__.py`
3. Create `packages/<name>/tests/`
4. Add to root `[tool.uv.sources]` if other packages depend on it
5. Run `uv sync`

## Adding an App

1. Create `apps/<name>/pyproject.toml` with `[project.scripts]` entry
2. Create `apps/<name>/src/<name>/main.py`
3. Add workspace dependencies via `[tool.uv.sources]`
4. Run `uv sync`
5. Execute with `uv run <name>`
