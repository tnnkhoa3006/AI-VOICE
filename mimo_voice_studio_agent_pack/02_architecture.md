# 02 - System Architecture

## High-level Architecture

User
-> Next.js Web App
-> FastAPI Backend
-> PostgreSQL
-> Redis Queue
-> Celery Worker
-> MiMo TTS API
-> Cloudflare R2
-> PostgreSQL update
-> Frontend receives job result

## Why Queue Is Required
Không gọi MiMo TTS trực tiếp trong HTTP request generate full audio vì:
- Audio có thể mất nhiều thời gian.
- Request dễ timeout.
- Không retry tốt.
- Khó kiểm soát credit/refund.
- Không scale được khi nhiều user.

## Services

### Web App
- Landing page.
- Dashboard.
- Studio editor.
- Project management.
- Audio player.
- Billing page.

### API Service
- Auth verify.
- Project CRUD.
- TTS job creation.
- Credit check.
- Job status.
- Voice profile.
- Billing webhook.

### Worker Service
- Consume TTS jobs.
- Call MiMo TTS.
- Decode base64 audio.
- Convert format if needed.
- Upload to R2.
- Update DB.
- Refund credit if failed.

### Storage Service
- Store generated audio.
- Store voice clone samples.
- Generate signed download URLs.

### AI Script Service
- Rewrite script.
- Split text into segments.
- Create style prompts.
- Suggest voice.

---

# Job Lifecycle

1. User requests TTS generation.
2. API validates:
   - user authenticated
   - text not empty
   - project exists
   - user owns project
   - enough credits
3. API creates tts_segment if needed.
4. API creates generation_job with status queued.
5. API deducts reserved credits.
6. API pushes Celery job.
7. Worker marks job processing.
8. Worker calls MiMo API.
9. Worker decodes audio.
10. Worker uploads audio to R2.
11. Worker updates segment audio_url.
12. Worker marks job completed.
13. Frontend polls job status or receives realtime event.
14. User plays/downloads audio.

## Failure Flow
1. Worker fails.
2. Retry according to policy.
3. If final failure:
   - mark job failed
   - save error message
   - refund reserved credits
   - show clear error in UI

---

# Recommended Monorepo Structure

mimo-voice-studio/
├── apps/
│   ├── web/
│   ├── api/
│   └── worker/
├── packages/
│   ├── contracts/
│   ├── prompts/
│   └── docs/
├── infra/
│   ├── docker-compose.yml
│   ├── nginx/
│   └── scripts/
└── agent-skills/
