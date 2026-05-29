import enum
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, JSON, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
  pass


def enum_values(enum_cls: type[enum.Enum]) -> list[str]:
  return [item.value for item in enum_cls]


class TimestampMixin:
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    onupdate=func.now(),
  )


class ProjectType(str, enum.Enum):
  quick_tts = "quick_tts"
  script_voice = "script_voice"
  dialogue = "dialogue"
  story = "story"
  elearning = "elearning"


class ProjectStatus(str, enum.Enum):
  active = "active"
  archived = "archived"


class VoiceProfileType(str, enum.Enum):
  built_in = "built_in"
  voice_design = "voice_design"
  voice_clone = "voice_clone"


class SegmentStatus(str, enum.Enum):
  draft = "draft"
  queued = "queued"
  processing = "processing"
  completed = "completed"
  failed = "failed"


class JobStatus(str, enum.Enum):
  queued = "queued"
  processing = "processing"
  completed = "completed"
  failed = "failed"
  cancelled = "cancelled"


class CreditTransactionType(str, enum.Enum):
  reserve = "reserve"
  consume = "consume"
  refund = "refund"
  purchase = "purchase"
  bonus = "bonus"


class User(Base, TimestampMixin):
  __tablename__ = "users"

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
  name: Mapped[str | None] = mapped_column(String(255), nullable=True)
  avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
  plan: Mapped[str] = mapped_column(String(50), default="free")
  credit_balance: Mapped[int] = mapped_column(Integer, default=1000)

  projects: Mapped[list["Project"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Project(Base, TimestampMixin):
  __tablename__ = "projects"

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
  title: Mapped[str] = mapped_column(String(255))
  type: Mapped[ProjectType] = mapped_column(Enum(ProjectType, values_callable=enum_values), default=ProjectType.quick_tts)
  status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus, values_callable=enum_values), default=ProjectStatus.active)

  user: Mapped[User] = relationship(back_populates="projects")
  segments: Mapped[list["TTSSegment"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class VoiceProfile(Base):
  __tablename__ = "voice_profiles"

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
  name: Mapped[str] = mapped_column(String(255))
  type: Mapped[VoiceProfileType] = mapped_column(Enum(VoiceProfileType, values_callable=enum_values), default=VoiceProfileType.built_in)
  provider: Mapped[str] = mapped_column(String(50), default="mimo")
  provider_model: Mapped[str | None] = mapped_column(String(120), nullable=True)
  provider_voice: Mapped[str | None] = mapped_column(String(120), nullable=True)
  design_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
  sample_audio_url: Mapped[str | None] = mapped_column(Text, nullable=True)
  consent_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TTSSegment(Base, TimestampMixin):
  __tablename__ = "tts_segments"

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), index=True)
  order_index: Mapped[int] = mapped_column(Integer, default=0)
  text: Mapped[str] = mapped_column(Text)
  voice_profile_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("voice_profiles.id"), nullable=True)
  voice_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
  style_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
  audio_url: Mapped[str | None] = mapped_column(Text, nullable=True)
  audio_format: Mapped[str] = mapped_column(String(12), default="wav")
  duration_seconds: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
  status: Mapped[SegmentStatus] = mapped_column(Enum(SegmentStatus, values_callable=enum_values), default=SegmentStatus.draft)

  project: Mapped[Project] = relationship(back_populates="segments")


class GenerationJob(Base):
  __tablename__ = "generation_jobs"

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
  project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), index=True)
  segment_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tts_segments.id"), nullable=True, index=True)
  provider: Mapped[str] = mapped_column(String(50), default="mimo")
  model: Mapped[str | None] = mapped_column(String(120), nullable=True)
  input_text: Mapped[str] = mapped_column(Text)
  style_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
  voice_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
  status: Mapped[JobStatus] = mapped_column(Enum(JobStatus, values_callable=enum_values), default=JobStatus.queued, index=True)
  reserved_credits: Mapped[int] = mapped_column(Integer, default=0)
  used_credits: Mapped[int | None] = mapped_column(Integer, nullable=True)
  output_audio_url: Mapped[str | None] = mapped_column(Text, nullable=True)
  error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
  retry_count: Mapped[int] = mapped_column(Integer, default=0)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
  started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
  completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class CreditTransaction(Base):
  __tablename__ = "credit_transactions"

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
  amount: Mapped[int] = mapped_column(Integer)
  type: Mapped[CreditTransactionType] = mapped_column(Enum(CreditTransactionType, values_callable=enum_values))
  reason: Mapped[str] = mapped_column(String(255))
  job_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("generation_jobs.id"), nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class Subscription(Base, TimestampMixin):
  __tablename__ = "subscriptions"

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
  provider: Mapped[str] = mapped_column(String(50))
  provider_customer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
  provider_subscription_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
  plan: Mapped[str] = mapped_column(String(80))
  status: Mapped[str] = mapped_column(String(80))
  current_period_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
  current_period_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class AudioAsset(Base):
  __tablename__ = "audio_assets"

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
  project_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True, index=True)
  segment_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tts_segments.id"), nullable=True, index=True)
  storage_key: Mapped[str] = mapped_column(Text)
  public_url: Mapped[str | None] = mapped_column(Text, nullable=True)
  mime_type: Mapped[str] = mapped_column(String(120))
  size_bytes: Mapped[int] = mapped_column(Integer)
  duration_seconds: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

