# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spendly is a Flask-based personal expense tracker web app. It's a learning/tutorial project with a polished frontend shell and route skeleton — backend logic (database, auth, CRUD) is stubbed out for incremental implementation across steps 1–9.

## Development Commands

```bash
# Activate virtual environment (Windows)
venv\Scripts\Activate.ps1      # PowerShell
venv\Scripts\activate.bat      # cmd

# Install dependencies
pip install -r requirements.txt

# Run the dev server (starts on http://localhost:5001)
python app.py

# Run tests
pytest
pytest path/to/test_file.py           # single file
pytest path/to/test_file.py::test_fn  # single test
```

## Architecture

- **app.py** — Single Flask application file. All routes defined here. Entry point via `python app.py` (debug mode, port 5001).
- **database/db.py** — Database module (stub). Intended to provide `get_db()`, `init_db()`, `seed_db()` for SQLite with `row_factory` and foreign keys enabled.
- **templates/** — Jinja2 templates extending `base.html`. Base layout provides shared navbar and footer.
- **static/css/style.css** — Complete design system using CSS custom properties (`--ink`, `--paper`, `--accent`, etc.). Typography: DM Serif Display (headings) + DM Sans (body) via Google Fonts.
- **static/js/main.js** — Client-side JavaScript (placeholder).

## Current Implementation State

**Working routes:** `/` (landing), `/register`, `/login`, `/terms`, `/privacy` — all GET-only, rendering templates.

**Stub routes** (return placeholder text, awaiting implementation):
- `/logout` (Step 3), `/profile` (Step 4)
- `/expenses/add` (Step 7), `/expenses/<id>/edit` (Step 8), `/expenses/<id>/delete` (Step 9)

Steps 1–2, 5–6 are implied (DB setup, auth wiring, session management) but don't have explicit route stubs.

## Key Conventions

- Database is SQLite (file: `expense_tracker.db`, gitignored).
- No ORM — raw SQL with `sqlite3` module and `row_factory`.
- No frontend frameworks or build tools — vanilla HTML/CSS/JS only.
- CSS uses a warm, editorial palette with variables in `:root`. Responsive breakpoints at 900px and 600px.
- Forms in templates use `.auth-card`, `.form-group`, `.form-input`, `.btn-submit` class conventions from the design system.
