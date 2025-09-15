import io, pandas as pd
from fastapi import APIRouter, UploadFile, File, Form, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..db import get_db, Base, engine
from ..models import Job, User
from ..cleaner import clean_dataframe
from ..storage import save_bytes, load_bytes
from ..reporting import build_pdf_report

router = APIRouter(prefix="/jobs", tags=["jobs"])
Base.metadata.create_all(bind=engine)

@router.post("/upload")
async def upload_job(
    file: UploadFile = File(...),
    email_columns: str = Form("email"),
    phone_columns: str = Form("phone"),
    key_columns: str = Form("email,phone"),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    emails = [c.strip() for c in email_columns.split(",") if c.strip()]
    phones = [c.strip() for c in phone_columns.split(",") if c.strip()]
    keys = [c.strip() for c in key_columns.split(",") if c.strip()]

    content = await file.read()
    df = pd.read_csv(io.BytesIO(content), dtype=str, keep_default_na=False)
    result = clean_dataframe(df, emails, phones, keys)

    buf = io.BytesIO()
    result["df"].to_csv(buf, index=False); buf.seek(0)
    storage_key = save_bytes(buf.read(), file.filename)

    job = Job(user_id=user.id, filename=file.filename, status="completed", summary_json=result["summary"], storage_key=storage_key)
    db.add(job); db.commit(); db.refresh(job)
    return {"job_id": job.id, "summary": job.summary_json}

@router.get("/list")
def list_jobs(db: Session = Depends(get_db), user = Depends(get_current_user)):
    jobs = db.query(Job).filter(Job.user_id == user.id).order_by(Job.created_at.desc()).all()
    return [{"id": j.id, "filename": j.filename, "created_at": j.created_at, "summary": j.summary_json} for j in jobs]

@router.get("/{job_id}/download")
def download(job_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    j = db.query(Job).filter(Job.id == job_id, Job.user_id == user.id).first()
    if not j: return {"error": "not found"}
    content = load_bytes(j.storage_key)
    return StreamingResponse(io.BytesIO(content), media_type="text/csv", headers={"Content-Disposition": f'attachment; filename="{j.filename.rsplit(".",1)[0]}_cleaned.csv"'})

@router.get("/{job_id}/report.pdf")
def pdf_report(job_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    j = db.query(Job).filter(Job.id == job_id, Job.user_id == user.id).first()
    if not j: return {"error": "not found"}
    pdf_bytes = build_pdf_report(j.summary_json or {})
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="job_{job_id}_report.pdf"'})
