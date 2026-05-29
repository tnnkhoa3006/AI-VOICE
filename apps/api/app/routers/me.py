from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import GenerationJob, JobStatus, User
from app.schemas import UsageRead, UserRead

router = APIRouter(tags=["user"])


@router.get("/me", response_model=UserRead)
def read_me(user: User = Depends(get_current_user)) -> User:
  return user


@router.get("/me/usage", response_model=UsageRead)
def read_usage(
  db: Session = Depends(get_db),
  user: User = Depends(get_current_user),
) -> UsageRead:
  completed_jobs = db.scalar(
    select(func.count(GenerationJob.id)).where(
      GenerationJob.user_id == user.id,
      GenerationJob.status == JobStatus.completed,
    )
  ) or 0
  return UsageRead(
    credit_balance=user.credit_balance,
    generated_seconds_this_month=0,
    generated_jobs_this_month=completed_jobs,
  )
