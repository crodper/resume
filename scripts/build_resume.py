#!/usr/bin/env python3

import argparse
import subprocess
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--template", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(args.data) as f:
        data = yaml.safe_load(f)

    
    env = Environment(
    loader=FileSystemLoader(Path(args.template).parent),
    autoescape=False,
    comment_start_string="((#",
    comment_end_string="#))",)
    
    env.globals.update({
        "latex": latex,
        "join_array": join_array,
        "format_phone": format_phone,
        "format_month": format_month,
        "cite": cite,
        "iso_country_name": iso_country_name,
        })



    template = env.get_template(Path(args.template).name)
    tex = template.render(**data)

    tex_file = out_dir / "resume.tex"
    with open(tex_file, "w") as f:
        f.write(tex)

    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", tex_file.name],
        cwd=out_dir,
        check=True
    )

if __name__ == "__main__":
    main()
