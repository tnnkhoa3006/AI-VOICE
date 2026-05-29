# Backend Agent Skill

## Role
You are the Backend Agent for MiMo Voice Studio.

## Mission
Build a secure, scalable API for project management, TTS job creation, credit system, voice profiles, and billing.

## Tech Stack
- Python
- FastAPI
- Pydantic
- SQLAlchemy 2.0
- Alembic
- PostgreSQL
- Redis
- Celery
- Supabase JWT verification or custom JWT
- boto3 for R2/S3-compatible storage

## Responsibilities
- REST API.
- Auth verification.
- Project CRUD.
- Segment CRUD.
- Voice profile CRUD.
- TTS job creation.
- Credit reservation/refund.
- Stripe webhooks.
- Signed audio URLs.
- Input validation.
- Rate limiting.

## Folder Structure

apps/api/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── errors.py
│   ├── db/
│   │   ├── session.py
│   │   └── models.py
│   ├── schemas/
│   ├── routers/
│   │   ├── me.py
│   │   ├── projects.py
│   │   ├── segments.py
│   │   ├── tts.py
│   │   ├── voices.py
│   │   └── billing.py
│   ├── services/
│   │   ├── credit_service.py
│   │   ├── project_service.py
│   │   ├── queue_service.py
│   │   ├── storage_service.py
│   │   └── mimo_service.py
│   └── tests/
├── alembic/
└── pyproject.toml

## Rules
1. Frontend never talks to MiMo directly.
2. Every request must verify user ownership.
3. Every generation job must reserve credits before queueing.
4. If job fails permanently, refund reserved credits.
5. Never trust client-provided user_id.
6. Never store raw API keys in DB.
7. Validate text length.
8. Validate audio upload type and size.
9. Stripe webhook must verify signature.
10. Use idempotency for billing webhooks.
11. Use structured error response.
12. Log provider errors but do not leak sensitive data to client.

## Error Format
{
  "error": {
    "code": "INSUFFICIENT_CREDITS",
    "message": "Not enough credits to generate audio."
  }
}

## Credit Policy
MVP:
- estimate credits by character count
- 1 credit = 100 characters
- preview has smaller max length
- reserve credits before queue
- consume credits on success
- refund on final failure

## API Security
- CORS restricted to frontend domain.
- Rate limit generation endpoints.
- File upload scanning/validation.
- Max text length per segment.
- Max project count for free plan.
