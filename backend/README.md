# GV Diagnostics API

## Setup

1. Create a PostgreSQL database and copy `.env.example` to `.env`.
2. From `backend/`, install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the initial schema migration:

```bash
alembic upgrade head
```

4. Start the API from the project root:

```bash
uvicorn app.main:app --app-dir backend --reload --port 8000
```

API documentation is available at `http://localhost:8000/docs`.

If SMTP or WhatsApp credentials are empty, submissions are still stored and the optional notification is skipped.
