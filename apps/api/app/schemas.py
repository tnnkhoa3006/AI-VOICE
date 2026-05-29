import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import JobStatus, ProjectStatus, ProjectType, SegmentStatus


class UserRead(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: uuid.UUID
  email: str
  name: str | None
  plan: str
  credit_balance: int


class UsageRead(BaseModel):
  credit_balance: int
  generated_seconds_this_month: int = 0
  generated_jobs_this_month: int = 0


class ProjectCreate(BaseModel):
  title: str = Field(min_length=1, max_length=255)
  type: ProjectType = ProjectType.quick_tts


class ProjectUpdate(BaseModel):
  title: str | None = Field(default=None, min_length=1, max_length=255)
  status: ProjectStatus | None = None


class ProjectRead(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: uuid.UUID
  title: str
  type: ProjectType
  status: ProjectStatus
  created_at: datetime
  updated_at: datetime


class SegmentCreate(BaseModel):
  text: str = Field(min_length=1)
  order_index: int = 0
  voice_name: str | None = None
  style_prompt: str | None = None
  audio_format: str = "wav"


class SegmentUpdate(BaseModel):
  text: str | None = Field(default=None, min_length=1)
  order_index: int | None = None
  voice_name: str | None = None
  style_prompt: str | None = None
  status: SegmentStatus | None = None


class SegmentRead(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: uuid.UUID
  project_id: uuid.UUID
  order_index: int
  text: str
  voice_name: str | None
  style_prompt: str | None
  audio_url: str | None
  audio_format: str
  status: SegmentStatus
  created_at: datetime
  updated_at: datetime


class TTSGenerateRequest(BaseModel):
  project_id: uuid.UUID
  segment_id: uuid.UUID | None = None
  text: str = Field(min_length=1, max_length=8000)
  voice_name: str = Field(min_length=1, max_length=120)
  style_prompt: str | None = Field(default=None, max_length=1000)
  format: str = Field(default="wav", pattern="^(wav|mp3)$")


class TTSQueuedResponse(BaseModel):
  job_id: uuid.UUID
  status: JobStatus


class TTSJobRead(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: uuid.UUID
  status: JobStatus
  output_audio_url: str | None
  error_message: str | None


class VoiceRead(BaseModel):
  id: str
  name: str
  type: str = "built_in"
  provider: str = "mimo"

