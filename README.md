# Resume Builder

A Python-based resume generator that converts YAML data into a polished LaTeX PDF using Jinja2 templates.

## Features

- ✨ **YAML-based**: Easy to maintain resume data in YAML format
- 🎨 **Customizable Templates**: Jinja2-powered LaTeX templates
- 🤖 **Automated CI/CD**: GitHub Actions builds and artifact generation
- 🔒 **Reproducible**: Exact dependencies and build process

## Prerequisites

- **Python 3.10+**
- **CMake 3.20+**
- **pdflatex** (part of TeX Live)

### System Dependencies Installation

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y cmake python3.10 python3-pip
sudo apt-get install -y texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

#### macOS
```bash
brew install cmake python@3.10 texlive
```

## Quick Start

### 1. Clone and Setup
```bash
git clone <repo-url>
cd resume
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Build Locally
```bash
# Create build directory and build PDF
cmake -B build
cmake --build build

# Output PDF location: build/resume.pdf
```

### 4. Update Your Resume
Edit `data/resume.yaml` with your information, then rebuild:
```bash
cmake --build build
```

## Project Structure

```
.
├── data/
│   └── resume.yaml           # Your resume data in YAML format
├── scripts/
│   ├── build_resume.py       # Main build script
│   └── helpers.py            # Jinja2 template helpers
├── templates/
│   └── resume.tex.j2         # LaTeX Jinja2 template
├── CMakeLists.txt            # CMake build configuration
├── requirements.txt          # Python dependencies
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
└── .github/workflows/        # GitHub Actions workflows
    └── build.yml             # CI/CD pipeline
```

## Development Workflow

### Setting Up Pre-commit Hooks

Pre-commit hooks automatically validate your changes before committing:

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

The hooks will:
- ✓ Validate YAML syntax
- ✓ Check Python code with ruff
- ✓ Fix trailing whitespace
- ✓ Ensure files end with newlines

### Running the Build Manually

```bash
# Full build with verbose output
cmake -B build -DCMAKE_VERBOSE_MAKEFILE=ON
cmake --build build
```

## CI/CD Pipeline

GitHub Actions automatically:
1. **On every push to main or PR**:
   - Validates Python dependencies
   - Installs LaTeX
   - Builds the PDF
   - Uploads PDF as artifact (retained 30 days)

2. **View Artifacts**:
   - Go to Actions → Latest workflow run → Artifacts section
   - Download `resume` artifact containing `resume.pdf`

## Troubleshooting

### Build Fails Locally
```bash
# Clean and rebuild
rm -rf build/
cmake -B build
cmake --build build
```

### pdflatex not found
Install TeX Live:
```bash
# Ubuntu/Debian
sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-latex-extra

# macOS
brew install texlive
```

### Python Dependencies Issue
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## License

See LICENSE file for details.
