from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from mdeck.cli import THEMES_DIR, cli


@pytest.fixture
def runner():
    return CliRunner()


def invoke(runner, args, meta=None, returncode=0):
    """Invoke the CLI with mocked frontmatter and subprocess."""
    mock_post = MagicMock()
    mock_post.metadata = meta or {}

    with patch("mdeck.cli.frontmatter.load", return_value=mock_post), \
         patch("mdeck.cli.subprocess.run", return_value=MagicMock(returncode=returncode)) as mock_run, \
         runner.isolated_filesystem():
        Path("slides.md").write_text("# Hello")
        result = runner.invoke(cli, ["slides.md"] + args)

    return result, mock_run


def _env(mock_run):
    return mock_run.call_args[1]["env"]


def _m_values(cmd):
    """Extract all values passed via -M flags from a command list."""
    return [cmd[i + 1] for i, arg in enumerate(cmd) if arg == "-M"]


# --- pdf-engine ---

def test_default_pdf_engine(runner):
    _, mock_run = invoke(runner, [])
    assert "--pdf-engine=lualatex" in mock_run.call_args[0][0]


def test_frontmatter_pdf_engine(runner):
    _, mock_run = invoke(runner, [], meta={"pdf-engine": "xelatex"})
    assert "--pdf-engine=xelatex" in mock_run.call_args[0][0]


def test_cli_pdf_engine_overrides_frontmatter(runner):
    _, mock_run = invoke(runner, ["--pdf-engine", "pdflatex"], meta={"pdf-engine": "xelatex"})
    cmd = mock_run.call_args[0][0]
    assert "--pdf-engine=pdflatex" in cmd
    assert "--pdf-engine=xelatex" not in cmd


# --- aspectratio ---

def test_default_aspectratio_injected_when_absent(runner):
    _, mock_run = invoke(runner, [])
    assert "aspectratio=169" in _m_values(mock_run.call_args[0][0])


def test_frontmatter_aspectratio_not_overridden(runner):
    _, mock_run = invoke(runner, [], meta={"aspectratio": 43})
    m_vals = _m_values(mock_run.call_args[0][0])
    assert not any("aspectratio" in v for v in m_vals)


def test_cli_aspectratio(runner):
    _, mock_run = invoke(runner, ["--aspectratio", "43"])
    assert "aspectratio=43" in _m_values(mock_run.call_args[0][0])


def test_cli_aspectratio_overrides_frontmatter(runner):
    _, mock_run = invoke(runner, ["--aspectratio", "43"], meta={"aspectratio": 169})
    assert "aspectratio=43" in _m_values(mock_run.call_args[0][0])


# --- theme ---

def test_no_theme_by_default(runner):
    _, mock_run = invoke(runner, [])
    assert not any("theme" in v for v in _m_values(mock_run.call_args[0][0]))


def test_cli_theme(runner):
    _, mock_run = invoke(runner, ["--theme", "Madrid"])
    assert "theme=Madrid" in _m_values(mock_run.call_args[0][0])


def test_frontmatter_theme_not_duplicated(runner):
    """Theme in frontmatter is read by pandoc natively; no extra -M injected."""
    _, mock_run = invoke(runner, [], meta={"theme": "metropolis"})
    assert not any("theme" in v for v in _m_values(mock_run.call_args[0][0]))


def test_cli_theme_overrides_frontmatter(runner):
    _, mock_run = invoke(runner, ["--theme", "Madrid"], meta={"theme": "metropolis"})
    assert "theme=Madrid" in _m_values(mock_run.call_args[0][0])


# --- output path ---

def test_default_output_path(runner):
    _, mock_run = invoke(runner, [])
    cmd = mock_run.call_args[0][0]
    assert cmd[cmd.index("-o") + 1].endswith("slides.pdf")


def test_custom_output_path(runner):
    _, mock_run = invoke(runner, ["-o", "out.pdf"])
    cmd = mock_run.call_args[0][0]
    assert cmd[cmd.index("-o") + 1] == "out.pdf"


# --- bundled themes ---

def test_texinputs_includes_themes_dir(runner):
    _, mock_run = invoke(runner, [])
    assert str(THEMES_DIR) in _env(mock_run)["TEXINPUTS"]


def test_texinputs_preserves_existing(runner):
    with patch.dict("os.environ", {"TEXINPUTS": "/custom/path"}):
        _, mock_run = invoke(runner, [])
    texinputs = _env(mock_run)["TEXINPUTS"]
    assert str(THEMES_DIR) in texinputs
    assert "/custom/path" in texinputs


def test_themes_dir_exists_and_has_sty_files():
    assert THEMES_DIR.is_dir()
    assert list(THEMES_DIR.glob("*.sty")), "No .sty files found in themes dir"


# --- dependency checks ---

def test_missing_pandoc(runner):
    with patch("mdeck.cli.shutil.which", side_effect=lambda cmd: None if cmd == "pandoc" else "/usr/bin/cmd"):
        result, _ = invoke(runner, [])
    assert result.exit_code != 0
    assert "pandoc" in result.output
    assert "pandoc.org" in result.output


def test_missing_pdf_engine(runner):
    with patch("mdeck.cli.shutil.which", side_effect=lambda cmd: None if cmd == "lualatex" else "/usr/bin/cmd"):
        result, _ = invoke(runner, [])
    assert result.exit_code != 0
    assert "lualatex" in result.output
    assert "tug.org" in result.output


def test_missing_custom_engine(runner):
    with patch("mdeck.cli.shutil.which", side_effect=lambda cmd: None if cmd == "pdflatex" else "/usr/bin/cmd"):
        result, _ = invoke(runner, ["--pdf-engine", "pdflatex"])
    assert result.exit_code != 0
    assert "pdflatex" in result.output


# --- error handling ---

def test_nonzero_returncode_propagates(runner):
    result, _ = invoke(runner, [], returncode=1)
    assert result.exit_code == 1


def test_missing_file(runner):
    result = runner.invoke(cli, ["nonexistent.md"])
    assert result.exit_code != 0
