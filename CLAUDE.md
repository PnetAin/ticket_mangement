# CLAUDE.md — Ticket Management Application

This file provides context for AI assistants working on this codebase. Read it before making any changes.

---

## Project Overview

A Flask-based ticket management web application with:
- CRUD operations for support tickets
- A "saved tickets" workflow
- LinkedIn post generation from tickets
- NLP utilities (spaCy) — partially implemented
- Jinja2-rendered HTML frontend with a JSON API layer

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Web Framework | Flask |
| ORM | Flask-SQLAlchemy (SQLAlchemy) |
| Migrations | Flask-Migrate (Alembic) |
| Database | SQLite (default, configurable) |
| NLP | spaCy (`en_core_web_sm`) |
| Templating | Jinja2 |
| Frontend | HTML5, CSS3, Vanilla JS |

> **Note:** `requirements.txt` is currently empty. The actual dependencies are:
> `flask`, `flask-sqlalchemy`, `flask-migrate`, `requests`, `spacy`
> Install with: `pip install flask flask-sqlalchemy flask-migrate requests spacy && python -m spacy download en_core_web_sm`

---

## Repository Structure

```
ticket_mangement/
├── run.py                      # Entry point — starts Flask dev server
├── config.py                   # Config class (reads env vars)
├── requirements.txt            # EMPTY — see Tech Stack above
├── README.md                   # Minimal project description
├── instance/
│   └── app.db                  # SQLite database (auto-created)
├── migrations/                 # Alembic migration scripts
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── b03f6392dff8_initial_migration.py   # Creates ticket table
│       └── 205061528756_add_saved_column_to_ticket.py  # Adds saved column
└── app/
    ├── __init__.py             # App factory: create_app()
    ├── models.py               # SQLAlchemy ORM models
    ├── routes/
    │   ├── __init__.py         # Home blueprint (GET /)
    │   ├── tickets.py          # Primary ticket routes (ACTIVE)
    │   ├── tickets2.py         # Duplicate/alternative ticket routes (see Known Issues)
    │   ├── linkedin.py         # LinkedIn post creation
    │   └── nlp.py              # NLP routes — EMPTY, not implemented
    ├── utils/
    │   ├── linkedin_api.py     # LinkedIn API client (placeholder tokens)
    │   └── nlp_tools.py        # spaCy NLP helper functions
    ├── static/
    │   ├── css/style.css.txt   # CSS (note: .txt extension — see Known Issues)
    │   └── js/script.js.txt    # JavaScript (note: .txt extension — see Known Issues)
    └── templates/
        ├── base.html           # Base layout — all templates extend this
        ├── index.html          # Home page
        ├── tickets.html        # Ticket list + create form
        ├── saved_tickets.html  # Saved tickets view
        └── edit_ticket.html    # Edit ticket form
```

---

## Development Setup

### 1. Install dependencies
```bash
pip install flask flask-sqlalchemy flask-migrate requests spacy
python -m spacy download en_core_web_sm
```

### 2. Configure environment variables (optional)
```bash
export SECRET_KEY="your-secret-key"
export DATABASE_URL="sqlite:///app.db"   # default; also accepts PostgreSQL URIs
```

### 3. Initialize / apply database migrations
```bash
flask db upgrade       # Apply all migrations to create/update schema
```

### 4. Run the development server
```bash
python run.py          # Starts Flask on http://127.0.0.1:5000 with debug=True
```

### Database migration workflow
```bash
flask db migrate -m "description of change"   # Auto-generate migration from model changes
flask db upgrade                               # Apply pending migrations
flask db downgrade                             # Revert last migration
```

---

## Configuration (`config.py`)

```python
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")   # Change in production
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

All configuration is read from environment variables with safe defaults for local development.

---

## Database Model

**Single model: `Ticket`** — defined in `app/models.py`

| Column | Type | Default | Notes |
|---|---|---|---|
| `id` | Integer | auto | Primary key |
| `title` | String(120) | required | Not nullable |
| `description` | Text | null | Optional |
| `notes` | Text | null | Optional additional notes |
| `status` | String(20) | `'Open'` | Values: `Open`, `In Progress`, `Closed` |
| `saved` | Boolean | `False` | Marks ticket as saved/bookmarked |
| `created_at` | DateTime | `now()` | Server-side default |

When adding new fields: create a model change in `app/models.py`, then run `flask db migrate` + `flask db upgrade`.

---

## API Routes

### Home Blueprint (`app/routes/__init__.py`)
| Method | Path | Handler | Description |
|---|---|---|---|
| GET | `/` | `home()` | Renders `index.html` |

### Tickets Blueprint (`app/routes/tickets.py`) — PRIMARY
| Method | Path | Handler | Description |
|---|---|---|---|
| GET | `/tickets` | `manage_tickets()` | Renders ticket list (`tickets.html`) |
| POST | `/tickets` | `manage_tickets()` | Creates a new ticket (sets `saved=True`) |
| GET | `/tickets/<id>` | `ticket_detail()` | Returns ticket as JSON |
| PUT | `/tickets/<id>` | `ticket_detail()` | Updates ticket fields (JSON body) |
| DELETE | `/tickets/<id>` | `ticket_detail()` | Deletes ticket, returns 204 |
| GET | `/saved-tickets` | `saved_tickets()` | Renders `saved_tickets.html` |
| GET | `/saved-ticket-ids` | `get_saved_ticket_ids()` | Returns JSON list of saved ticket IDs + titles |
| GET | `/tickets/<id>/edit` | `edit_ticket()` | Renders edit form (`edit_ticket.html`) |
| POST | `/tickets/<id>/edit` | `edit_ticket()` | Saves edits, redirects to `/tickets` |

### LinkedIn Blueprint (`app/routes/linkedin.py`)
| Method | Path | Handler | Description |
|---|---|---|---|
| POST | `/linkedin/post` | `create_linkedin_post()` | Creates LinkedIn post from ticket data |

> **Warning:** LinkedIn integration uses hardcoded placeholder values (`"your_access_token"`, `"urn:li:person:your-profile-id"`). It is not functional without real credentials.

### NLP Blueprint (`app/routes/nlp.py`)
- File exists but contains no routes. Not yet implemented.

---

## Code Conventions

### Python / Flask
- **App factory pattern**: `create_app()` in `app/__init__.py` creates and configures the Flask app. Never import `app` directly from module level — always use the factory.
- **Blueprint modularization**: Each feature area gets its own blueprint registered in `create_app()`. Follow the existing pattern when adding new route files.
- **Snake_case** for all functions and variables; **PascalCase** for classes.
- JSON responses for API-style endpoints (`/tickets/<id>` GET/PUT/DELETE), HTML template rendering for page routes.

### Database
- All model changes must be reflected in a migration. Never alter `instance/app.db` manually.
- Use `db.session.add()` + `db.session.commit()` for writes.
- Use `db.session.get(Model, id)` (SQLAlchemy 2.x style) for primary key lookups.

### Templates
- All templates extend `base.html` using `{% extends "base.html" %}`.
- Use `{% block content %}` for page-specific content.
- Forms POST to the same URL; route handlers differentiate by `request.method`.

### Static files
- CSS lives in `app/static/css/`, JS in `app/static/js/`.
- Reference via `url_for('static', filename='css/style.css')` in templates.

---

## Known Issues / Tech Debt

1. **Empty `requirements.txt`** — Dependencies are not pinned. Add all imports to requirements.txt when making changes.

2. **Duplicate route files** — `tickets.py` and `tickets2.py` both define `/tickets` routes. `tickets.py` is the active one registered in `create_app()`. `tickets2.py` appears to be an experimental copy and should be reconciled or removed.

3. **Static file extensions** — `style.css.txt` and `script.js.txt` have `.txt` extensions which will cause incorrect MIME types. Rename to `.css` and `.js` respectively and update template references.

4. **Hardcoded LinkedIn credentials** — `app/utils/linkedin_api.py` contains placeholder tokens. Move to environment variables before enabling LinkedIn features.

5. **No CSRF protection** — Forms have no CSRF tokens. Add `Flask-WTF` or equivalent before deploying.

6. **Default `SECRET_KEY`** — The fallback `"default_secret_key"` must never be used in production. Always set `SECRET_KEY` via environment variable.

7. **Empty NLP routes** — `app/routes/nlp.py` is a stub. Either implement or remove it.

8. **No tests** — Zero test coverage. Add `pytest` and `pytest-flask` when writing new features.

---

## Git Workflow

- **Main branch:** `main`
- **Feature branches:** `claude/<description>` (e.g. `claude/add-claude-documentation-nv4A9`)
- Commits are GPG/SSH signed automatically via git config.
- Always push feature branches to `origin` with `-u`: `git push -u origin <branch-name>`
- Do NOT push directly to `main` without a pull request.
