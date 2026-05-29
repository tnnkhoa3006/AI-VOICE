# 10 - Project Rules

## General Development Rules
1. Build MVP first, do not over-engineer.
2. Keep frontend, backend, worker boundaries clear.
3. No provider API key in frontend.
4. Every generation action creates a job.
5. Every job has a status.
6. Every user-facing error must be understandable.
7. Every paid/credit action must be auditable.
8. Logs must not contain API keys or full private audio URLs.
9. Do not store unnecessary personal data.
10. Prefer simple, explicit code over clever abstraction.

## Git Rules
Branch naming:
- feature/<short-name>
- fix/<short-name>
- chore/<short-name>

Commit format:
- feat: add project creation
- fix: refund credits on failed job
- chore: update docker compose
- refactor: extract storage service
- test: add tts job tests

## Pull Request Checklist
- Feature works manually.
- Tests added/updated.
- No API key committed.
- Migration included if schema changed.
- Error states handled.
- Loading states handled.
- Ownership checks included.
- Documentation updated if needed.

## Code Style
Frontend:
- TypeScript strict.
- Components under 250 lines when possible.
- Use server state via TanStack Query.
- Use local state only for UI/editor.

Backend:
- Pydantic schemas for request/response.
- Services contain business logic.
- Routers stay thin.
- DB transactions for credit/job changes.
- Alembic migration for schema changes.

Worker:
- Idempotent jobs.
- Safe retries.
- Clean temp files.
- Update final status.

## Environment Variables
Required:
- DATABASE_URL
- REDIS_URL
- MIMO_API_KEY
- R2_ACCOUNT_ID
- R2_ACCESS_KEY_ID
- R2_SECRET_ACCESS_KEY
- R2_BUCKET_NAME
- STRIPE_SECRET_KEY
- STRIPE_WEBHOOK_SECRET
- FRONTEND_URL
- SENTRY_DSN

## Definition of Done
A feature is done only when:
- UI works.
- API works.
- Worker flow works if applicable.
- Error state handled.
- Tests exist.
- No secrets exposed.
- Docs updated.
