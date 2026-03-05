# mdeck

**Beautiful PDF slide decks from Markdown.** No LaTeX knowledge required.

Write your talk in plain Markdown, run one command, get a professional-looking presentation — powered by [Beamer](https://ctan.org/pkg/beamer) and the [Metropolis](https://github.com/matze/mtheme) theme, which is bundled so you don't have to install anything extra.

```sh
mdeck talk.md --open
```

---

## Get started in 2 minutes

**1. Install dependencies**

```sh
brew install pandoc
brew install --cask mactex   # or any TeX distribution with LuaLaTeX
```

**2. Install mdeck**

```sh
pipx install mdeck
```

**3. Write your talk**

```markdown
---
title: "My Talk"
author: Jane Doe
date: "June 2025"
theme: metropolis
---

# Motivation

Why this problem matters.

# Approach

- Key idea one
- Key idea two

# Results

Lorem ipsum.
```

**4. Build**

```sh
mdeck talk.md --open
```

That's it. No `\begin{frame}`, no preamble, no `.cls` files to hunt down.

---

## How it works

Each `# Heading` in your Markdown becomes a slide. Everything else is standard Markdown: bullet lists, bold, italics, code blocks, images. Under the hood, mdeck calls pandoc with the right flags so you never have to.

---

## Customisation

Options can go in the file's YAML frontmatter, on the command line, or both. **CLI flags always win.**

### Frontmatter

| Key | Default | Values |
|-----|---------|--------|
| `theme` | *(beamer default)* | Any Beamer theme; `metropolis` is bundled |
| `aspectratio` | `169` | `43` `169` `1610` `149` `54` `32` |
| `pdf-engine` | `lualatex` | `lualatex` `xelatex` `pdflatex` |
| `mainfont` | — | Any font name (LuaLaTeX/XeLaTeX only) |
| `title` / `author` / `date` | — | Free text |

### CLI

```
mdeck [OPTIONS] FILE

  -o, --output PATH               Output PDF path  (default: FILE.pdf)
  --theme TEXT                    Beamer theme
  --aspectratio [43|169|1610|...]  Slide aspect ratio
  --pdf-engine TEXT               PDF engine
  --open                          Open the PDF after building
  --version                       Show version
  --help                          Show help
```
