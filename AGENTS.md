# AGENTS.md - Resume Builder Development Guide

This file provides coding standards and operational guidelines for agentic coding tools (Cursor, Copilot, Claude) working in this repository.

## Project Overview

**Resume Builder**: A Python-based resume generator converting YAML data into polished LaTeX PDFs using Jinja2 templates. Built with CMake orchestration and GitHub Actions CI/CD automation.

**Tech Stack**: Python 3.10+, CMake 3.20+, LaTeX, Jinja2, YAML

---

## Build & Execution Commands

### Setup
```bash
pip install -r requirements.txt
sudo apt-get install -y texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

### Build Resume PDF
```bash
cmake -B build          # Create build directory
cmake --build build     # Execute build (runs Python script -> LaTeX -> PDF)
```

### Clean Build
```bash
rm -rf build/           # Clean all artifacts
cmake -B build && cmake --build build
```

### Manual Script Execution (Testing)
```bash
python scripts/build_resume.py \
  --data data/resume.yaml \
  --template templates/resume.tex.j2 \
  --out build/
```

### Validate YAML Data
```bash
python -m yaml data/resume.yaml      # Basic validation
yamllint -d relaxed data/resume.yaml  # Strict validation
```

### Code Quality & Linting
```bash
ruff check scripts/                   # Lint Python code
ruff format scripts/                  # Auto-format Python
ruff check scripts/ --fix             # Fix issues automatically
```

### Pre-commit Hooks
```bash
pre-commit install                    # Setup hooks (one-time)
pre-commit run --all-files            # Run all hooks manually
pre-commit run yamllint --all-files   # Run specific hook
```

### CI/CD Verification (Local)
```bash
# Simulate GitHub Actions workflow locally:
python -m pip install --upgrade pip
pip install -r requirements.txt
yamllint data/resume.yaml
ruff check scripts/ --fix
cmake -B build && cmake --build build
ls -lh build/resume.pdf  # Verify output
```

---

## Code Style Guidelines

### Python Code Standards

#### Imports
- Use alphabetical order, group by: stdlib → third-party → local
- Example:
  ```python
  import argparse
  import subprocess
  import sys
  from pathlib import Path
  
  import yaml
  from jinja2 import Environment, FileSystemLoader
  
  from helpers import (
      cite,
      format_month,
      format_phone,
      iso_country_name,
      join_array,
      latex,
  )
  ```
- Max line length: 100 characters (enforced by Ruff)

#### Formatting & Style
- **Line length**: Max 100 chars (Ruff default)
- **Indentation**: 4 spaces (no tabs)
- **Naming conventions**:
  - Variables/functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`
  - Private functions: prefix with `_`

#### Type Hints
- Use type hints for all function signatures
- Example:
  ```python
  def validate_inputs(args: argparse.Namespace) -> None:
      """Validate input arguments and files."""
      if not args.data or not args.template or not args.out:
          raise ValueError("Arguments required")
  ```
- Return type `-> None` for functions with no return
- Use `from pathlib import Path` instead of string paths

#### Docstrings
- Use triple-quoted docstrings for all functions/classes
- Single-line format for simple functions:
  ```python
  def join_array(sep: str, items: list) -> str:
      """Join array items with separator."""
  ```
- Multi-line for complex functions:
  ```python
  def validate_inputs(args: argparse.Namespace) -> None:
      """Validate input arguments and files.
      
      Raises:
          ValueError: If required arguments missing
          FileNotFoundError: If data or template files don't exist
      """
  ```

#### Error Handling
- **Prefer specific exceptions** over generic `Exception`
- Example:
  ```python
  try:
      result = subprocess.run(..., check=True, capture_output=True)
  except subprocess.CalledProcessError as e:
      print(f"❌ Process failed: {e.returncode}")
      raise
  except FileNotFoundError:
      print("❌ pdflatex not found")
      raise
  ```
- Always provide context in error messages with file paths
- Use f-strings for all string formatting

#### Logging & Output
- Use `print()` for user-facing messages (this repo style)
- Include emoji prefixes for clarity: `🔍`, `✓`, `❌`, `📂`, `⚙️`, `✅`
- Always print status messages before long operations
- Errors to stderr: `print(..., file=sys.stderr)`

### YAML Data Format

#### Structure Requirements
```yaml
basics:
  name: String
  title: String
  email: String (use plain email, no +tags)
  phone: String
  github: String (full HTTPS URL)
  linkedin: String (full HTTPS URL)
  label: String
  summary: |
    Multi-line text with hashtags

work:
  - name: Company Name
    position: Job Title
    url: String (HTTPS)
    startDate: "YYYY-MM"
    endDate: "present" or "YYYY-MM"
    summary: String
    highlights:
      - Bullet point 1
      - Bullet point 2

skills:
  - name: Category Name
    keywords:
      - Skill 1
      - Skill 2
```

#### YAML Best Practices
- Use **2-space indentation** (YAML standard)
- String values without special characters: unquoted
- URLs and emails: quoted strings
- Multi-line text: use `|` (literal block) or `>` (folded block)
- Dates: `"YYYY-MM"` format (quoted)
- Always validate: `yamllint -d strict data/resume.yaml`

### LaTeX Template Best Practices

#### Jinja2 Syntax in Templates
- Variable interpolation: `{{ variable }}`
- Filters: `{{ array | join(", ") }}`
- Conditionals: `{% if condition %} ... {% endif %}`
- Loops: `{% for item in items %} ... {% endfor %}`
- Comments: `((# comment text #))` (custom delimiters to avoid LaTeX conflicts)

#### Template Patterns
- Access nested YAML: `{{ basics.name }}`, `{{ work[0].position }}`
- Use Jinja2 filters for formatting: `{{ latex("textbf", text) }}`
- Call Python helpers: `{{ iso_country_name(code, "en") }}`

---

## Repository Structure

```
.
├── data/
│   └── resume.yaml              # Resume data (source of truth)
├── scripts/
│   ├── build_resume.py          # Main build script (entry point)
│   └── helpers.py               # Jinja2 template helpers
├── templates/
│   └── resume.tex.j2            # LaTeX Jinja2 template
├── .github/workflows/
│   ├── ci.yml                   # Build + test workflow
│   └── release.yml              # GitHub release automation
├── CMakeLists.txt               # Build configuration
├── requirements.txt             # Python dependencies
├── .pre-commit-config.yaml      # Pre-commit hooks
└── AGENTS.md                    # This file
```

---

## Common Workflows for Agents

### Adding New Features
1. **Update YAML structure** in `data/resume.yaml` if needed
2. **Add template logic** in `templates/resume.tex.j2`
3. **Add helper function** in `scripts/helpers.py` if formatting needed
4. **Update `build_resume.py`** for input validation
5. **Test locally**: `cmake -B build && cmake --build build`
6. **Run linters**: `ruff check scripts/ --fix && yamllint data/resume.yaml`
7. **Commit**: `git add . && git commit -m "feat: description"`

### Debugging Build Failures
```bash
# 1. Check YAML syntax
yamllint -d strict data/resume.yaml

# 2. Run Python script with verbose output
python scripts/build_resume.py \
  --data data/resume.yaml \
  --template templates/resume.tex.j2 \
  --out build/

# 3. Check CMake configuration
cmake -B build -DCMAKE_VERBOSE_MAKEFILE=ON

# 4. Inspect generated LaTeX
cat build/resume.tex

# 5. Check pdflatex logs
tail -100 build/resume.log
```

---

## Pre-commit Hooks Configuration

**Active hooks** (from `.pre-commit-config.yaml`):
- `trailing-whitespace`: Remove trailing spaces
- `end-of-file-fixer`: Ensure files end with newline
- `check-yaml`: Validate YAML syntax
- `yamllint`: Strict YAML linting (line length max 120)
- `ruff`: Python linting & auto-fix
- `ruff-format`: Python auto-formatting

**Installation**: `pre-commit install` (run once)

**Manual execution**: `pre-commit run --all-files`

---

## Git Workflow

### Commit Message Format
```
<type>: <description>

<optional details>

Closes #<issue-number> (if applicable)
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `ci`

Example:
```
feat: add support for custom LaTeX commands

- Extend helpers.py with new LaTeX formatting functions
- Update template to use new commands
- Add validation in build_resume.py

Closes #42
```

### Branch Strategy
- **main**: Production-ready (protected)
- Feature branches: `feature/description` (created from main)
- Always create a commit before pushing

### Git Push Policy ⚠️
- **AGENTS MUST NOT PUSH COMMITS AUTOMATICALLY**
- Agents should create commits locally when explicitly requested
- Agents must show what they've done and ask for approval before pushing
- Only push to remote (`git push`) after user explicitly approves
- No exceptions - always wait for user confirmation before `git push`

---

## Key Files to Edit

| File | Purpose | Notes |
|------|---------|-------|
| `data/resume.yaml` | Resume content | Single source of truth |
| `templates/resume.tex.j2` | PDF layout | Jinja2 + LaTeX syntax |
| `scripts/build_resume.py` | Build logic | Error handling + validation |
| `scripts/helpers.py` | Template helpers | Pure functions for formatting |
| `CMakeLists.txt` | Build orchestration | Rarely needs changes |
| `requirements.txt` | Python dependencies | Update when adding packages |

---

## CI/CD Pipeline (GitHub Actions)

**Workflows** (in `.github/workflows/`):
- `ci.yml`: Runs on every push/PR - builds PDF, uploads artifact (30 days)
- `release.yml`: Runs on tags `v*` - creates GitHub Release with PDF assets

**Important**: Always test locally before pushing to avoid failed CI runs.

---

## Performance Considerations

- **YAML parsing**: `yaml.safe_load()` is safe and efficient
- **Jinja2 rendering**: Template rendering is fast (~100ms)
- **pdflatex**: Slowest step (~2-3 seconds), runs once per build
- **CI/CD**: Total runtime ~30 seconds (install + build + validate)

---

## Questions? Issues?

For urgent issues with builds:
1. Check error messages (they include file paths)
2. Run `pre-commit run --all-files` locally
3. Verify YAML with `yamllint -d strict data/resume.yaml`
4. Review CI logs in GitHub Actions
