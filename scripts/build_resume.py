#!/usr/bin/env python3

import argparse
import subprocess
import sys
import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

from helpers import (
    latex,
    join_array,
    format_phone,
    format_month,
    cite,
    iso_country_name,
)


def validate_inputs(args):
    """Validate input arguments and files."""
    if not args.data or not args.template or not args.out:
        raise ValueError("Arguments --data, --template, and --out are required")
    
    data_path = Path(args.data)
    template_path = Path(args.template)
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")


def main():
    parser = argparse.ArgumentParser(description="Build resume PDF from YAML data and Jinja2 template")
    parser.add_argument("--data", required=True, help="Path to resume YAML data file")
    parser.add_argument("--template", required=True, help="Path to Jinja2 template file")
    parser.add_argument("--out", required=True, help="Output directory for generated files")
    args = parser.parse_args()

    try:
        # Validate inputs
        print("🔍 Validating inputs...")
        validate_inputs(args)
        
        out_dir = Path(args.out)
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Output directory: {out_dir}")

        # Load YAML data
        print(f"📂 Loading data from {args.data}...")
        with open(args.data) as f:
            data = yaml.safe_load(f)
        print(f"✓ Data loaded successfully")

        # Setup Jinja2 environment
        print(f"📋 Setting up template engine...")
        env = Environment(
            loader=FileSystemLoader(Path(args.template).parent),
            autoescape=False,
            comment_start_string="((#",
            comment_end_string="#))",
        )
        
        env.globals.update({
            "latex": latex,
            "join_array": join_array,
            "format_phone": format_phone,
            "format_month": format_month,
            "cite": cite,
            "iso_country_name": iso_country_name,
        })
        print(f"✓ Template engine ready")

        # Render template
        print(f"🎨 Rendering template...")
        template = env.get_template(Path(args.template).name)
        tex = template.render(**data)
        print(f"✓ Template rendered")

        # Write LaTeX file
        tex_file = out_dir / "resume.tex"
        print(f"✍️  Writing LaTeX file to {tex_file}...")
        with open(tex_file, "w") as f:
            f.write(tex)
        print(f"✓ LaTeX file written")

        # Run pdflatex
        print(f"⚙️  Running pdflatex...")
        try:
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_file.name],
                cwd=out_dir,
                check=True,
                capture_output=True,
                text=True
            )
            print(f"✓ pdflatex completed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ pdflatex failed with exit code {e.returncode}")
            print("STDOUT:", e.stdout[-500:] if e.stdout else "")
            print("STDERR:", e.stderr[-500:] if e.stderr else "")
            raise
        except FileNotFoundError:
            print("❌ pdflatex not found. Please install texlive-latex-base")
            raise

<<<<<<< HEAD
        # Verify PDF was generated
        pdf_file = out_dir / "resume.pdf"
        if not pdf_file.exists():
            raise RuntimeError(f"PDF file was not generated at {pdf_file}")
        print(f"✅ Resume PDF generated successfully at {pdf_file}")
        print(f"📊 File size: {pdf_file.stat().st_size / 1024:.1f} KB")

    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
=======
    tex_file = out_dir / "CarlosRodriguezPeralta_resume.tex"
    with open(tex_file, "w") as f:
        f.write(tex)
>>>>>>> 02a238920cbaee8300356c7c756276fb87fe3b73


if __name__ == "__main__":
    main()
