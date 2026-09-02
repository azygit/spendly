# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Spendly — a Flask personal expense tracker. This repo is a step-by-step course scaffold: many features are intentionally unimplemented placeholders, marked in comments with which "Step" they belong to (e.g. `app.py` routes return literal strings like `"Add expense — coming in Step 7"`; `database/db.py` has a docstring-only stub for Step 1). When asked to implement a feature, check for one of these markers first — it tells you the intended shape of the work.

## Commands

```bash
source venv/bin/activate        # virtualenv already created, deps installed here
python3 app.py                  # run the dev server on http://localhost:5001 (debug=True)
pytest                          # run tests (no test files exist yet)
pytest path/to/test_file.py::test_name   # run a single test
```

There is no build step, linter, or frontend toolchain — templates and static assets are served directly by Flask.

## Architecture

- **`app.py`** — single Flask app, all routes defined at module level (no blueprints). Implemented routes render templates directly (`/`, `/register`, `/login`, `/terms`, `/privacy`); unimplemented ones (`/logout`, `/profile`, `/expenses/...`) are stubs returning plain strings, awaiting the database layer.
- **`database/db.py`** — intended to hold `get_db()` (SQLite connection with `row_factory` + foreign keys on), `init_db()`, and `seed_db()`. Not yet implemented — currently just a comment describing the contract future code must satisfy. There's no ORM; expect raw SQLite.
- **`templates/`** — Jinja2, all pages extend `base.html`. `base.html` owns the `<nav>` and `<footer>` (footer contains the Terms/Privacy links) and exposes `{% block title %}`, `{% block head %}`, `{% block content %}`, `{% block scripts %}` for child templates to fill.
- **`static/css/style.css`** — one stylesheet for the whole site, organized in `/* ---- Section ---- */` comment blocks (Navbar, Hero, Dashboard mock, Buttons, Features, CTA, Auth pages, Legal pages, Demo modal, Responsive). Design tokens (colors, fonts, radii, max-width) are CSS custom properties in `:root`. When editing one section of the UI, keep changes scoped to its comment block rather than touching shared tokens or unrelated blocks.
- **`static/js/main.js`** — vanilla JS only, no frontend framework/build step. Current content: an IIFE wiring up the landing-page "See how it works" demo modal (opens/closes an embedded YouTube iframe, clearing its `src` on close so the video actually stops).
- No authentication, sessions, or persistence are wired up yet — `/register` and `/login` templates render forms that POST to routes not yet defined in `app.py`.
