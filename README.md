# Ticket Management Application

A Flask-based web application for managing support tickets, with saved ticket workflows, LinkedIn post generation, and NLP utilities.

## Features

- Create, view, edit, and delete support tickets
- Save/bookmark tickets for quick access
- Generate LinkedIn posts from ticket data
- NLP utilities powered by spaCy (in progress)
- JSON API layer alongside a Jinja2-rendered frontend

## Tech Stack

- **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-Migrate
- **Database:** SQLite (configurable via `DATABASE_URL`)
- **NLP:** spaCy (`en_core_web_sm`)
- **Frontend:** Jinja2 templates, HTML5, CSS3, Vanilla JavaScript

## Getting Started

### 1. Install dependencies

```bash
pip install flask flask-sqlalchemy flask-migrate requests spacy
python -m spacy download en_core_web_sm
```

### 2. Configure environment variables (optional)

```bash
export SECRET_KEY="your-secret-key"
export DATABASE_URL="sqlite:///app.db"   # default
```

### 3. Apply database migrations

```bash
flask db upgrade
```

### 4. Run the development server

```bash
python run.py
```

The app will be available at `http://127.0.0.1:5000`.

## Project Structure

```
ticket_mangement/
├── run.py              # Entry point
├── config.py           # Configuration (reads env vars)
├── app/
│   ├── __init__.py     # App factory: create_app()
│   ├── models.py       # Ticket model
│   ├── routes/         # Blueprint route handlers
│   ├── utils/          # LinkedIn API client, NLP helpers
│   ├── static/         # CSS and JavaScript
│   └── templates/      # Jinja2 HTML templates
└── migrations/         # Alembic database migrations
```

## API Overview

| Method | Path | Description |
|--------|------|-------------|
| GET | `/tickets` | List all tickets |
| POST | `/tickets` | Create a new ticket |
| GET | `/tickets/<id>` | Get ticket (JSON) |
| PUT | `/tickets/<id>` | Update ticket (JSON) |
| DELETE | `/tickets/<id>` | Delete ticket |
| GET | `/saved-tickets` | View saved tickets |
| POST | `/linkedin/post` | Generate a LinkedIn post |

## Database

Tickets have the following fields: `id`, `title`, `description`, `notes`, `status` (`Open` / `In Progress` / `Closed`), `saved`, `created_at`.

To add a new field:

```bash
# 1. Edit app/models.py
flask db migrate -m "describe the change"
flask db upgrade
```
