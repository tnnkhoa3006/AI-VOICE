# 01 - Technology Stack

## Main Recommendation

Vì app xử lý audio, queue, storage, billing và có khả năng scale, stack nên chia module rõ:

## Frontend
Recommended:
- Next.js
- React
- TailwindCSS
- shadcn/ui
- TanStack Query
- Zustand hoặc Jotai
- WaveSurfer.js cho audio waveform
- React Hook Form + Zod

Why:
- Build nhanh.
- SEO tốt cho landing page.
- Dashboard/editor dễ làm.
- Component ecosystem mạnh.

Alternative nếu muốn không JS-heavy:
- SvelteKit cho frontend nhẹ hơn.
- Flutter Web nếu sau này muốn chung code với mobile.
- Vue/Nuxt nếu bạn thích Vue.

Final frontend choice:
- Next.js + React + Tailwind + shadcn/ui.

---

## Backend API
Recommended:
- Go + Fiber/Gin
hoặc
- Python + FastAPI
hoặc
- Kotlin + Ktor
hoặc
- NestJS

Best balanced choice:
- FastAPI nếu muốn xử lý AI/audio dễ, code nhanh.
- Go nếu muốn hiệu năng, worker nhẹ, deploy gọn.
- NestJS nếu muốn full TypeScript monorepo.

Final backend choice đề xuất:
- FastAPI cho API.
- Python worker cho audio.
- PostgreSQL.
- Redis queue.

Why FastAPI:
- Tích hợp AI/audio/FFmpeg dễ.
- Pydantic validate tốt.
- Swagger tự sinh.
- Code ngắn, rõ.
- Dễ viết worker chung Python.

---

## Worker
Recommended:
- Python worker + Celery + Redis
hoặc
- Dramatiq + Redis
hoặc
- RQ + Redis

Final choice:
- Celery + Redis.

Why:
- Xử lý background job ổn.
- Có retry, status, queue.
- Phù hợp tác vụ generate audio.

---

## Database
Recommended:
- PostgreSQL

ORM:
- SQLAlchemy 2.0 + Alembic
hoặc
- Prisma nếu dùng TS.

Final:
- PostgreSQL + SQLAlchemy + Alembic.

---

## Storage
Recommended:
- Cloudflare R2
hoặc
- AWS S3
hoặc
- MinIO local dev.

Final:
- Cloudflare R2 production.
- MinIO local dev.

Why:
- Rẻ.
- S3-compatible.
- Lưu audio tốt.

---

## Auth
Options:
- Clerk
- Auth.js
- Supabase Auth
- Custom JWT

Final:
- Supabase Auth nếu muốn nhanh.
hoặc
- Custom JWT nếu muốn kiểm soát toàn bộ.

MVP recommendation:
- Supabase Auth + backend verify JWT.

---

## Payment
- Stripe.

## Audio Processing
- FFmpeg.
- pydub nếu dùng Python.
- librosa chỉ dùng khi cần phân tích audio nâng cao.

## Observability
- Sentry.
- PostHog.
- OpenTelemetry về sau.

## Deployment
MVP:
- Frontend: Vercel
- Backend: Railway/Fly.io/Render
- DB: Neon/Supabase Postgres
- Redis: Upstash
- Storage: Cloudflare R2

Scale:
- Docker Compose dev.
- Production deploy bằng Kubernetes hoặc ECS/Fargate.

---

# Final Stack

## Recommended Production Stack
- Frontend: Next.js + TailwindCSS + shadcn/ui
- Backend: Python FastAPI
- Worker: Python Celery
- Queue: Redis
- Database: PostgreSQL
- ORM: SQLAlchemy 2.0
- Migration: Alembic
- Storage: Cloudflare R2
- Audio: FFmpeg
- Auth: Supabase Auth
- Payment: Stripe
- Monitoring: Sentry + PostHog
