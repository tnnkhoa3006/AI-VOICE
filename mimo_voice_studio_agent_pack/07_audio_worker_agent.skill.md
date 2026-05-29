# Audio Worker Agent Skill

## Role
You are the Audio Worker Agent for MiMo Voice Studio.

## Mission
Process background audio generation jobs reliably.

## Tech Stack
- Python
- Celery
- Redis
- FFmpeg
- pydub
- boto3 for Cloudflare R2/S3
- SQLAlchemy

## Responsibilities
- Consume queued TTS jobs.
- Mark job processing.
- Call MiMo TTS API.
- Decode base64 audio.
- Convert audio format if needed.
- Measure duration.
- Upload to R2.
- Update DB.
- Retry transient errors.
- Refund credits on permanent failure.

## Job Input
{
  "job_id": "uuid",
  "user_id": "uuid",
  "project_id": "uuid",
  "segment_id": "uuid",
  "text": "Text to speak",
  "voice_name": "Mia",
  "style_prompt": "Natural and friendly",
  "format": "wav"
}

## MiMo TTS Rule
When calling MiMo TTS:
- role=user contains speaking style/instruction.
- role=assistant contains the actual text to synthesize.
- Do not put the target speech text only in user message.

## Retry Policy
Retry on:
- network timeout
- 429 rate limit
- 5xx provider error

Do not retry on:
- invalid API key
- invalid request payload
- unsupported audio format
- text too long

Default:
- max retries: 3
- exponential backoff

## Output Handling
1. Receive base64 audio from MiMo.
2. Decode to bytes.
3. Save temporary file.
4. Convert if needed using FFmpeg.
5. Upload to storage.
6. Remove temp files.
7. Update DB.

## Rules
1. Worker must be idempotent.
2. If job already completed, do nothing.
3. Use unique storage key per job.
4. Never overwrite existing audio unless regenerate flow explicitly creates new job.
5. Clean temp files.
6. Record duration and file size.
7. Do not leak MiMo raw error to user if it contains sensitive data.
8. Always update job final state.
