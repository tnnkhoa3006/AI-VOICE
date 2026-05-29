# MiMo Voice Studio

AI Voice Studio MVP for turning ideas or scripts into generated voice-over audio.

## Stack

- Frontend: Next.js, React, TailwindCSS, TanStack Query, shadcn-style UI primitives
- Backend: FastAPI, SQLAlchemy 2.0, Alembic
- Worker: Celery with Redis
- Database: PostgreSQL
- Storage: local dev storage first, R2/S3-compatible storage later
- Audio provider: MiMo TTS through backend and worker only

## Local Setup

1. Copy `.env.example` to `.env`.
2. Start infrastructure and services:

```bash
docker compose up --build
```

3. Open:

- Web: http://localhost:3000
- API docs: http://localhost:8000/docs
- MinIO console: http://localhost:9001

## Rules

- The frontend never calls MiMo directly.
- Every audio generation request creates a job.
- Jobs move through `queued`, `processing`, `completed`, or `failed`.
- Credits are reserved first and refunded on final failure.
- Generated audio is stored as an asset, not in the database.

