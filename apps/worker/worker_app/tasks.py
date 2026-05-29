import uuid
from datetime import UTC, datetime

from app.db import SessionLocal
from app.models import AudioAsset, GenerationJob, JobStatus, SegmentStatus, TTSSegment, User
from app.queue import celery_app
from app.services.credits import consume_credits, refund_credits
from app.services.mimo import MimoTTSClient
from app.services.storage import StorageService


@celery_app.task(bind=True, name="worker.generate_tts_audio", max_retries=3)
def generate_tts_audio(self, job_id: str) -> dict[str, str]:
  parsed_job_id = uuid.UUID(job_id)

  with SessionLocal() as db:
    job = db.get(GenerationJob, parsed_job_id)
    if not job:
      return {"status": "missing"}

    if job.status in {JobStatus.completed, JobStatus.failed, JobStatus.cancelled}:
      return {"status": job.status.value}

    segment = db.get(TTSSegment, job.segment_id) if job.segment_id else None
    job.status = JobStatus.processing
    job.started_at = job.started_at or datetime.now(UTC)
    if segment:
      segment.status = SegmentStatus.processing
    db.commit()

    try:
      voice_payload = job.voice_payload or {}
      audio_format = voice_payload.get("format", "wav")
      result = MimoTTSClient().synthesize(
        text=job.input_text,
        voice_name=voice_payload.get("voice_name", "Mia"),
        style_prompt=job.style_prompt,
        audio_format=audio_format,
      )
      extension = "mp3" if result.mime_type == "audio/mpeg" else "wav"
      storage_key = f"audio/{job.user_id}/{job.id}.{extension}"
      audio_url = StorageService().save_audio(storage_key, result.audio, result.mime_type)

      job.status = JobStatus.completed
      job.output_audio_url = audio_url
      job.completed_at = datetime.now(UTC)
      db.add(consume_credits(job))

      if segment:
        segment.status = SegmentStatus.completed
        segment.audio_url = audio_url
        segment.audio_format = extension
        segment.duration_seconds = result.duration_seconds

      db.add(
        AudioAsset(
          user_id=job.user_id,
          project_id=job.project_id,
          segment_id=job.segment_id,
          storage_key=storage_key,
          public_url=audio_url,
          mime_type=result.mime_type,
          size_bytes=len(result.audio),
          duration_seconds=result.duration_seconds,
        )
      )
      db.commit()
      return {"status": "completed"}

    except Exception as exc:
      job.retry_count += 1

      if self.request.retries >= self.max_retries:
        user = db.get(User, job.user_id)
        job.status = JobStatus.failed
        job.error_message = str(exc)
        job.completed_at = datetime.now(UTC)
        if segment:
          segment.status = SegmentStatus.failed
        if user:
          db.add(refund_credits(user, job))
        db.commit()
        return {"status": "failed"}

      db.commit()
      raise self.retry(exc=exc, countdown=min(60, 5 * (self.request.retries + 1)))

