from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import get_db
from app.models import User


def get_or_create_dev_user(db: Session, email: str) -> User:
  user = db.scalar(select(User).where(User.email == email))
  if user:
    return user

  user = User(email=email, name=email.split("@")[0], credit_balance=1000)
  db.add(user)
  db.commit()
  db.refresh(user)
  return user


def get_current_user(
  db: Session = Depends(get_db),
  authorization: str | None = Header(default=None),
  dev_user_email: str | None = Header(default=None, alias="X-Dev-User-Email"),
) -> User:
  if settings.auth_dev_bypass:
    return get_or_create_dev_user(db, dev_user_email or settings.dev_user_email)

  if not isinstance(authorization, str) or not authorization.startswith("Bearer "):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

  raise HTTPException(
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    detail="Supabase JWT verification is not configured yet",
  )
