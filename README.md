# GV Diagnostic Services — Website

Modern responsive diagnostic-lab website starter built with React + Vite + Framer Motion + Lucide React.

## Run

```bash
npm install
npm run dev
```

Production build:

```bash
npm run build
npm run preview
```

## Full-stack setup

The frontend submits bookings and contact messages to the FastAPI backend through `VITE_API_URL`.

1. Install frontend dependencies: `npm install`
2. Install backend dependencies: `pip install -r backend/requirements.txt`
3. Create a PostgreSQL database and copy `backend/.env.example` to `backend/.env`.
4. Run migrations from the project root: `alembic upgrade head`
5. Start FastAPI: `uvicorn app.main:app --app-dir backend --reload --port 8000`
6. Start React: `npm run dev`
7. Open `http://localhost:5173`
8. Open API documentation at `http://localhost:8000/docs`

Set `VITE_API_URL` in a root `.env` file when the API is not running at the default local URL. SMTP and WhatsApp notifications are optional; when unconfigured, submissions remain stored in the database.

## Edit first

- `src/config/site.js` — company details, phone numbers, social URLs and images.
- `src/main.jsx` — services, tests, doctors, reviews and page content.
- `src/styles.css` — visual design.
- `public/images/` — put final licensed company images here. See `public/images/README.txt` for the exact filenames.

## Current contact details used

- Company: GV Diagnostic Services
- Main phone: 9866020079
- Phone and home pickup: 9866020079

## Editable demo content

The specialists and testimonials are explicitly marked as placeholders. Replace them with verified GV Diagnostics information before launch. The technology section uses abstract capabilities rather than unconfirmed partner logos.

Booking and contact forms now validate in the browser and submit to the backend. They display a generated reference number after a successful API response and a user-safe error message when the backend is unavailable.

The visual placeholder images are referenced from online sources so the layout can be previewed. For a commercial launch, use images the company owns or has licensed and preferably store them locally.
