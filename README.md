# ClearPoint SaaS Starter

A production-ready FastAPI starter for ClearPoint Data Services with:
- ✅ Auth (JWT) & users
- ✅ Job uploads, cleaning pipeline, PDF report
- ✅ Job history per client
- ✅ Stripe subscription stubs
- ✅ S3 storage hooks (local fallback by default)
- ✅ Phone validation (libphonenumber), email verification hook
- ✅ Docker image & .env config

## Quick Start (Local)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # edit secrets if you want
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/auth-docs to create a user and fetch a token.

## Core Endpoints
- `POST /auth/register` – create user
- `POST /auth/token` – get JWT (OAuth2 Password)
- `GET /auth/me` – current user
- `POST /jobs/upload` – upload CSV (auth required)
- `GET /jobs/list` – list my jobs
- `GET /jobs/{id}/download` – download cleaned CSV
- `GET /jobs/{id}/report.pdf` – PDF report
- `GET /billing/config` – Stripe public config
- `POST /billing/checkout` – create Checkout session (requires Stripe keys)

## Config (.env)
- `APP_SECRET` – long random string
- `DB_URL` – default SQLite
- Stripe keys (optional): `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, price IDs, webhook secret
- S3 keys (optional): set to enable S3; otherwise local ./storage is used

## Production Notes
- Put behind a reverse proxy (Nginx) and add HTTPS
- Use Postgres in production
- Add S3 and Stripe keys to enable cloud storage & billing
- Add a scheduler worker (e.g., APScheduler/Celery) for recurring cleanups
- Add proper email verification provider via API (ZeroBounce/Hunter)

## Roadmap
- Admin dashboard, usage quotas, CSV/Excel templates
- OAuth SSO (Google), rate limiting, audit logs
- CRM integrations (HubSpot/Salesforce)
