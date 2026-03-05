# mdeck roadmap

## Completed
- [x] CLI tool (`src/mdeck/cli.py`) with click — converts Markdown to Beamer PDF
- [x] Bundled Metropolis theme (`.sty` files in `src/mdeck/themes/`) with TEXINPUTS injection
- [x] Dependency checks for `pandoc` and pdf-engine with actionable install hints
- [x] `--version` flag via `@click.version_option(package_name="mdeck")`
- [x] README written for user conversion
- [x] 21 unit tests (pytest + CliRunner, all mocked)

## Pending

### For users
- [ ] **Demo GIF in README** — screen recording of Markdown → PDF; highest-converting README addition
- [ ] **PyPI publication + GitHub Actions** — CI on push, publish workflow on tag; `pipx install mdeck` needs this
- [ ] **`pyproject.toml` completeness** — add `license`, `keywords`, `classifiers`, `homepage`, `repository` for PyPI listing
- [ ] **Watch mode (`--watch`)** — rebuild on save; tightest part of the writing loop
- [ ] **Starter template (`mdeck init`)** — scaffolds a `slides.md` with common frontmatter pre-filled

### For AI agents / scripting
- [ ] **`--quiet` flag** — suppresses pandoc stderr so agents rely on exit codes alone
- [ ] **stdin support (`mdeck -`)** — pipe Markdown directly without a temp file
- [ ] **Structured errors (`--json`)** — machine-parseable failure output on stderr
