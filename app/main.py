from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from .models import User
from .auth import get_current_user, hash_password
from .routes.auth_routes import router as auth_router
from .routes.jobs_routes import router as jobs_router
from .routes.stripe_routes import router as stripe_router

app = FastAPI(title="ClearPoint SaaS Starter", version="0.2.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# create tables
Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def home(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

@app.get("/setup", response_class=HTMLResponse)
def setup(request: Request, db: Session = Depends(get_db)):
    # seed an admin if none exists
    if not db.query(User).first():
        admin = User(email="admin@clearpointdataservices.com", name="Admin", hashed_password=hash_password("admin123"), role="admin")
        db.add(admin); db.commit()
    return RedirectResponse(url="/auth-docs")

@app.get("/auth-docs", response_class=HTMLResponse)
def auth_docs(request: Request):
    return templates.TemplateResponse("auth_docs.html", {"request": request})

# Routers
app.include_router(auth_router)
app.include_router(jobs_router)
app.include_router(stripe_router)

@app.get("/healthz")
def healthz():
    return {"ok": True}
