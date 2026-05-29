import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import GenerationJob, JobStatus, Project, TTSSegment, User
from app.queue import celery_app
from app.schemas import TTSGenerateRequest, TTSJobRead, TTSQueuedResponse
from app.services.credits import estimate_credits, refund_credits, reserve_credits

router = APIRouter(prefix="/tts", tags=["tts"])


def ensure_project_owner(db: Session, project_id: uuid.UUID, user_id: uuid.UUID) -> Project:
  project = db.scalar(select(Project).where(Project.id == project_id, Project.user_id == user_id))
  if not project:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
  return project


def enqueue_tts_job(payload: TTSGenerateRequest, db: Session, user: User, preview: bool) -> TTSQueuedResponse:
  ensure_project_owner(db, payload.project_id, user.id)

  segment_id = None if preview else payload.segment_id
  if segment_id:
    segment = db.scalar(
      select(TTSSegment)
      .join(Project)
      .where(TTSSegment.id == segment_id, Project.user_id == user.id)
    )
    if not segment:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Segment not found")

  job = GenerationJob(
    user_id=user.id,
    project_id=payload.project_id,
    segment_id=segment_id,
    input_text=payload.text,
    style_prompt=payload.style_prompt,
    voice_payload={"voice_name": payload.voice_name, "format": payload.format, "preview": preview},
    status=JobStatus.queued,
  )
  db.add(job)
  db.flush()

  credits = estimate_credits(payload.text)
  try:
    transaction = reserve_credits(user, job, credits)
  except ValueError as exc:
    raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(exc)) from exc

  db.add(transaction)
  db.commit()
  db.refresh(job)

  try:
    celery_app.send_task("worker.generate_tts_audio", args=[str(job.id)])
  except Exception as exc:
    job.status = JobStatus.failed
    job.error_message = "Queue is unavailable"
    db.add(refund_credits(user, job))
    db.commit()
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Queue is unavailable") from exc

  return TTSQueuedResponse(job_id=job.id, status=job.status)


@router.post("/preview", response_model=TTSQueuedResponse)
def generate_preview(
  payload: TTSGenerateRequest,
  db: Session = Depends(get_db),
  user: User = Depends(get_current_user),
) -> TTSQueuedResponse:
  return enqueue_tts_job(payload, db, user, preview=True)


@router.post("/generate", response_model=TTSQueuedResponse)
def generate_audio(
  payload: TTSGenerateRequest,
  db: Session = Depends(get_db),
  user: User = Depends(get_current_user),
) -> TTSQueuedResponse:
  return enqueue_tts_job(payload, db, user, preview=False)


@router.get("/jobs/{job_id}", response_model=TTSJobRead)
def read_tts_job(
  job_id: uuid.UUID,
  db: Session = Depends(get_db),
  user: User = Depends(get_current_user),
) -> GenerationJob:
  job = db.scalar(select(GenerationJob).where(GenerationJob.id == job_id, GenerationJob.user_id == user.id))
  if not job:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
  return job
