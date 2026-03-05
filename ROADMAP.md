# mdeck roadmap

## Completed
- [x] CLI tool (`src/mdeck/cli.py`) with click — converts Markdown to Beamer PDF
- [x] Bundled Metropolis theme (`.sty` files in `src/mdeck/themes/`) with TEXINPUTS injection
- [x] Dependency checks for `pandoc` and pdf-engine with actionable install hints
- [x] `--version` flag via `@click.version_option(package_name="mdeck")`
- [x] README written for user conversion
- [x] 21 unit tests (pytest + CliRunner, all mocked)
- [x] `pyproject.toml` completeness — license, keywords, classifiers, URLs
- [x] MIT license
- [x] GitHub repo at https://github.com/luiscruz/mdeck
- [x] PyPI package built — pending `twine upload` with API token

## Pending

### For users
- [ ] **Demo GIF in README** — screen recording of Markdown → PDF; highest-converting README addition
- [ ] **GitHub Actions** — CI on push, publish workflow on tag
- [ ] **Watch mode (`--watch`)** — rebuild on save; tightest part of the writing loop
- [ ] **Starter template (`mdeck init`)** — scaffolds a `slides.md` with common frontmatter pre-filled

### For AI agents / scripting
- [ ] **`--quiet` flag** — suppresses pandoc stderr so agents rely on exit codes alone
- [ ] **stdin support (`mdeck -`)** — pipe Markdown directly without a temp file
- [ ] **Structured errors (`--json`)** — machine-parseable failure output on stderr

### Quality / compatibility
- [ ] **Shell completions** — expose Click's built-in completion generation for bash/zsh/fish via `mdeck --install-completion`
- [ ] **Windows compatibility** — `TEXINPUTS` separator is `;` on Windows vs `:` on Unix; currently broken on Windows
- [ ] **Custom theme directory (`--theme-dir`)** — let users point to their own `.sty` files instead of only the bundled Metropolis
- [ ] **Integration test** — a single end-to-end test that actually invokes pandoc and builds a PDF, to catch regressions in pandoc flags
