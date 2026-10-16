# python-template

Python monorepo template with the [Astral](https://astral.sh/) toolchain.

## Stack

- **[uv](https://docs.astral.sh/uv/)** — package manager, workspaces, Python version management
- **[ruff](https://docs.astral.sh/ruff/)** — linter and formatter
- **[ty](https://docs.astral.sh/ty/)** — type checker
- **[pytest](https://docs.pytest.org/)** — test runner
- **[lefthook](https://github.com/evilmartians/lefthook)** — git hooks
- **[mise](https://mise.jdx.dev/)** — pinned, checksum-locked dev tools (`mise.toml`, `mise.lock`)

## Usage

### From GitHub template

Click **"Use this template"** on GitHub, then:

```bash
git clone <your-new-repo>
cd <your-new-repo>
mise install --locked   # uv, ruff, ty, lefthook, jq, ripgrep
uv run python scripts/setup.py
uv sync
```

### With gh CLI

```bash
gh repo create my-project --template alleneubank/python-template --public --clone
cd my-project
mise install --locked
uv run python scripts/setup.py
uv sync
```

See [SETUP.md](SETUP.md) for details.

Tools come from [mise](https://mise.jdx.dev/): `mise.toml` pins exact versions and `mise.lock` pins
per-platform checksums. After cloning, run `mise trust` once. Tools are on `PATH` when mise is activated
in your shell or through direnv (`.envrc` runs `use mise`); otherwise prefix commands with `mise exec --`.

## Development

```bash
mise install --locked            # install pinned tools (direnv activates them via .envrc)
uv sync                          # install dependencies
uv run pytest                    # run tests
uv run ruff check .              # lint
uv run ruff format .             # format
uv run ty check                  # type check
uv run example                   # run example app
```

## Structure

```
apps/           # applications
  example/      # example app
packages/       # shared libraries
  core/         # core library
  utils/        # utility library
```

## License

MIT
