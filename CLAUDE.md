# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Python-based resume generator: YAML data → Jinja2 template → LaTeX → PDF. Orchestrated via CMake with GitHub Actions CI/CD.

**Stack**: Python 3.10+, CMake 3.20+, pdflatex, Jinja2, YAML

## Commands

### Build
```bash
cmake -B build && cmake --build build   # Full build → build/resume.pdf
rm -rf build/                           # Clean build artifacts
```

### Manual script execution (bypasses CMake)
```bash
python scripts/build_resume.py \
  --data data/resume.yaml \
  --template templates/resume.tex.j2 \
  --out build/
```

### Linting & validation
```bash
ruff check scripts/          # Lint Python
ruff check scripts/ --fix    # Lint + auto-fix
ruff format scripts/         # Format Python
yamllint -d strict data/resume.yaml   # Validate YAML
```

### Pre-commit hooks
```bash
pre-commit install            # One-time setup
pre-commit run --all-files    # Run all hooks
```

### Debugging a failed build
```bash
cat build/resume.tex          # Inspect generated LaTeX
tail -100 build/resume.log    # Check pdflatex output
```

## Architecture

The build pipeline has three stages:

1. **`scripts/build_resume.py`** — entry point. Loads `data/resume.yaml`, sets up Jinja2 environment with custom helpers, renders `templates/resume.tex.j2` → `build/resume.tex`, then invokes `pdflatex`.
2. **`scripts/helpers.py`** — pure functions registered as Jinja2 globals: `latex()`, `escape_latex()`, `join_array()`, `format_month()`, `format_phone()`, `cite()`, `iso_country_name()`.
3. **`templates/resume.tex.j2`** — Jinja2 template producing LaTeX. Uses custom comment delimiters `((# ... #))` to avoid conflicts with LaTeX syntax.

**CMake** (`CMakeLists.txt`) simply wires the dependency graph: if `resume.yaml`, the template, or `build_resume.py` change, CMake re-runs the Python script.

### Adding new template helpers
1. Add a pure function to `scripts/helpers.py`
2. Import it in `scripts/build_resume.py`
3. Register it in `env.globals.update({...})`
4. Use it in `templates/resume.tex.j2` as `{{ function_name(...) }}`

### LaTeX special characters
All user content must go through `escape_latex()` or `join_array()` before being emitted into the template to avoid LaTeX compilation errors.

## Key Files

| File | Role |
|------|------|
| `data/resume.yaml` | Single source of truth for resume content |
| `templates/resume.tex.j2` | PDF layout (Jinja2 + LaTeX) |
| `scripts/build_resume.py` | Build orchestration and validation |
| `scripts/helpers.py` | Formatting helpers for templates |

## Code Style

- Max line length: 100 chars (enforced by Ruff)
- Type hints required on all function signatures
- Use `pathlib.Path` instead of string paths
- `print()` for user-facing output; prefix messages with emoji (`✓`, `❌`, `📂`, etc.)
- Errors to `sys.stderr`

## YAML Format

- Dates: `"YYYY-MM"` (quoted strings)
- `endDate`: either `"YYYY-MM"` or `"present"`
- URLs and emails: quoted strings

## Git Policy

**Do not push commits automatically.** Create commits locally when explicitly asked, then wait for user approval before running `git push`.

Commit message format: `<type>: <description>` where type is one of `feat`, `fix`, `refactor`, `docs`, `test`, `ci`.
