# 11 - MVP Task Board

## Milestone 1 - Project Setup
- [ ] Create monorepo.
- [ ] Setup Next.js app.
- [ ] Setup FastAPI app.
- [ ] Setup Celery worker.
- [ ] Setup PostgreSQL.
- [ ] Setup Redis.
- [ ] Setup Docker Compose.
- [ ] Setup env examples.

## Milestone 2 - Auth and User
- [ ] Setup Supabase Auth or custom JWT.
- [ ] Backend auth middleware.
- [ ] GET /me.
- [ ] Protected dashboard route.
- [ ] User record sync.

## Milestone 3 - Projects and Segments
- [ ] Project model.
- [ ] Segment model.
- [ ] Project CRUD API.
- [ ] Segment CRUD API.
- [ ] Dashboard project list.
- [ ] Studio editor page.

## Milestone 4 - MiMo TTS Integration
- [ ] MiMo service.
- [ ] TTS job model.
- [ ] Credit transaction model.
- [ ] POST /tts/generate.
- [ ] Celery worker consumes job.
- [ ] Decode audio base64.
- [ ] Upload to local MinIO/R2.
- [ ] GET /tts/jobs/{id}.
- [ ] Frontend polling.

## Milestone 5 - Audio UX
- [ ] Audio player.
- [ ] Download button.
- [ ] Job status badge.
- [ ] Failed job retry.
- [ ] Preview generation.

## Milestone 6 - Credits
- [ ] Credit balance.
- [ ] Reserve credits.
- [ ] Consume credits.
- [ ] Refund failed job.
- [ ] Usage page.

## Milestone 7 - Polish
- [ ] Landing page.
- [ ] Empty states.
- [ ] Error states.
- [ ] Loading skeletons.
- [ ] Responsive UI.
- [ ] Sentry.
- [ ] Basic analytics.

## Milestone 8 - Optional Monetization
- [ ] Stripe checkout.
- [ ] Stripe webhook.
- [ ] Plan limits.
- [ ] Monthly credit reset.

## MVP Launch Criteria
- User can sign in.
- User can create a project.
- User can create a segment.
- User can generate audio.
- User can play audio.
- User can download audio.
- Failed job does not consume credits.
- API key is not exposed.
