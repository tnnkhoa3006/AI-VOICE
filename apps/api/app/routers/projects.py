import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Project, TTSSegment, User
from app.schemas import ProjectCreate, ProjectRead, ProjectUpdate, SegmentCreate, SegmentRead, SegmentUpdate

router = APIRouter(tags=["projects"])


def get_owned_project(db: Session, user: User, project_id: uuid.UUID) -> Project:
  project = db.scalar(
    select(Project).where(Project.id == project_id, Project.user_id == user.id)
  )
  if not project:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
  return project


def get_owned_segment(db: Session, user: User, segment_id: uuid.UUID) -> TTSSegment:
  segment = db.scalar(
    select(TTSSegment)
    .join(Project)
    .where(TTSSegment.id == segment_id, Project.user_id == user.id)
  )
  if not segment:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Segment not found")
  return segment


@router.post("/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
  payload: ProjectCreate,
  db: Session = Depends(get_db),
  user: User = Depends(get_current_user),
) -> Project:
  project = Project(user_id=user.id, title=payload.title, type=payload.type)
  db.add(project)
  db.commit()
  db.refresh(project)
  return project


@router.get("/projects", response_model=list[ProjectRead])
def list_projects(
  db: Session = Depends(get_db),
  user: User = Depends(get_current_user),
) -> list[Project]:
  return list(db.scalars(select(Project).where(Project.user_id == user.id).order_by(Project.updated_at.desc())))


@router.get("/projects/{project_id}", response_model=ProjectRead)
def read_project(
  project_id: uuid.UUID,
  db: Session = Depends(get_db),
  user: User = Depends(get_current_user),
) -> Project:
  return get_owned_project(db, user, project_id)


@router.patch("/projects/{project_id}", response_model=ProjectRead)
def update_project(
  project_id: uuid.UUID,
  payload: ProjectUpdate,
  db: Session = Depends(get_db),
  user: User = Depends(get_current_user),
) -> Project:
  project = get_owned_project(db, user, project_id)
  for field, value in payload.model_dump(exclude_unset=True).items():
    setattr(project, field, value)
  db.commit()
  db.refresh(project)
  return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
  project_id: uuid.UUID,
  db: Session = Depends(get_db),
  user: User = Depends(get_current_user),
) -> None:
  project = get_owned_project(db, user, project_id)
  db.delete(project)
  db.commit()


@router.post("/projects/{project_id}/segments", response_model=SegmentRead, status_code=status.HTTP_201_CREATED)
def create_segment(
  project_id: uuid.UUID,
  payload: SegmentCreate,
  db: Session = Depends(get_db),
  user: User = Depends(get_current_user),
) -> TTSSegment:
  get_owned_project(db, user, project_id)
  segment = TTSSegment(project_id=project_id, **payload.model_dump())
  db.add(segment)
  db.commit()
  db.refresh(segment)
  return segment


@router.patch("/segments/{segment_id}", response_model=SegmentRead)
def update_segment(
  segment_id: uuid.UUID,
  payload: SegmentUpdate,
  db: Session = Depends(get_db),
  user: User = Depends(get_current_user),
) -> TTSSegment:
  segment = get_owned_segment(db, user, segment_id)
  for field, value in payload.model_dump(exclude_unset=True).items():
    setattr(segment, field, value)
  db.commit()
  db.refresh(segment)
  return segment


@router.delete("/segments/{segment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_segment(
  segment_id: uuid.UUID,
  db: Session = Depends(get_db),
  user: User = Depends(get_current_user),
) -> None:
  segment = get_owned_segment(db, user, segment_id)
  db.delete(segment)
  db.commit()
