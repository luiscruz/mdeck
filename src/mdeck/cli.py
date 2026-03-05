import os
import shutil
import subprocess
import sys
from pathlib import Path

import click
import frontmatter

INSTALL_HINTS = {
    "pandoc": "Install pandoc: https://pandoc.org/installing.html  (macOS: brew install pandoc)",
    "lualatex": "Install a TeX distribution: https://tug.org/texlive/  (macOS: brew install --cask mactex)",
    "pdflatex": "Install a TeX distribution: https://tug.org/texlive/  (macOS: brew install --cask mactex)",
    "xelatex": "Install a TeX distribution: https://tug.org/texlive/  (macOS: brew install --cask mactex)",
}

THEMES_DIR = Path(__file__).parent / "themes"

DEFAULTS = {
    "pdf-engine": "lualatex",
    "aspectratio": "169",
}


def _require(cmd: str) -> None:
    if shutil.which(cmd) is None:
        hint = INSTALL_HINTS.get(cmd, f"Make sure '{cmd}' is installed and on your PATH.")
        raise click.ClickException(f"'{cmd}' not found. {hint}")


def _load_meta(path: Path) -> dict:
    try:
        return frontmatter.load(path).metadata
    except Exception:
        return {}


@click.command()
@click.version_option(package_name="markdeck")
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("-o", "--output", type=click.Path(path_type=Path), default=None,
              help="Output PDF path (default: FILE.pdf)")
@click.option("--pdf-engine", default=None,
              help=f"PDF engine (default: {DEFAULTS['pdf-engine']})")
@click.option("--theme", default=None, help="Beamer theme")
@click.option("--aspectratio", default=None,
              type=click.Choice(["43", "169", "1610", "149", "54", "32"]),
              help=f"Slide aspect ratio (default: {DEFAULTS['aspectratio']})")
@click.option("--open", "open_after", is_flag=True, default=False,
              help="Open the PDF after building")
def cli(file, output, pdf_engine, theme, aspectratio, open_after):
    """Convert a Markdown file to a Beamer PDF presentation."""
    meta = _load_meta(file)

    resolved_engine = pdf_engine or meta.get("pdf-engine") or DEFAULTS["pdf-engine"]
    output = output or file.with_suffix(".pdf")

    _require("pandoc")
    _require(resolved_engine)

    cmd = [
        "pandoc", str(file),
        "-t", "beamer",
        "-s",
        "-o", str(output),
        f"--pdf-engine={resolved_engine}",
    ]

    # Aspectratio: inject default only when absent from frontmatter
    if aspectratio:
        cmd += ["-M", f"aspectratio={aspectratio}"]
    elif "aspectratio" not in meta:
        cmd += ["-M", f"aspectratio={DEFAULTS['aspectratio']}"]

    # Theme: CLI overrides frontmatter; if absent from both, pandoc uses its default
    if theme:
        cmd += ["-M", f"theme={theme}"]

    env = os.environ.copy()
    env["TEXINPUTS"] = f"{THEMES_DIR}:{env.get('TEXINPUTS', '')}"

    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        sys.exit(result.returncode)

    if open_after:
        click.launch(str(output))
