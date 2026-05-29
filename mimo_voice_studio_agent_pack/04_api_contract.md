# 04 - API Contract

Base URL:
- /api/v1

Auth:
- Authorization: Bearer <access_token>

## User

GET /me
Response:
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "Khoa",
  "plan": "free",
  "credit_balance": 1000
}

GET /me/usage
Response:
{
  "credit_balance": 1000,
  "generated_seconds_this_month": 120,
  "generated_jobs_this_month": 10
}

---

## Projects

POST /projects
Body:
{
  "title": "TikTok Ads Voice",
  "type": "quick_tts"
}

GET /projects

GET /projects/{project_id}

PATCH /projects/{project_id}
Body:
{
  "title": "New title"
}

DELETE /projects/{project_id}

---

## Segments

POST /projects/{project_id}/segments
Body:
{
  "text": "Hello world",
  "order_index": 0,
  "voice_name": "Mia",
  "style_prompt": "Natural and friendly"
}

PATCH /segments/{segment_id}

DELETE /segments/{segment_id}

---

## TTS Jobs

POST /tts/preview
Body:
{
  "project_id": "uuid",
  "text": "Preview text",
  "voice_name": "Mia",
  "style_prompt": "Warm and natural",
  "format": "wav"
}

Response:
{
  "job_id": "uuid",
  "status": "queued"
}

POST /tts/generate
Body:
{
  "project_id": "uuid",
  "segment_id": "uuid",
  "text": "Full text",
  "voice_name": "Mia",
  "style_prompt": "Warm and natural",
  "format": "wav"
}

GET /tts/jobs/{job_id}
Response:
{
  "id": "uuid",
  "status": "completed",
  "output_audio_url": "https://...",
  "error_message": null
}

POST /tts/generate-all
Body:
{
  "project_id": "uuid",
  "segment_ids": ["uuid1", "uuid2"]
}

---

## Voices

GET /voices

POST /voices/design
Body:
{
  "name": "Young energetic male",
  "design_prompt": "A young Vietnamese male voice, warm, energetic, clear"
}

POST /voices/clone
multipart/form-data:
- name
- sample_audio
- consent_confirmed

DELETE /voices/{voice_id}

---

## Script AI

POST /script/rewrite
Body:
{
  "input": "rough idea",
  "template": "tiktok_ads",
  "tone": "energetic",
  "duration_seconds": 30
}

POST /script/split
Body:
{
  "script": "long script",
  "max_chars_per_segment": 500
}

POST /script/suggest-style
Body:
{
  "script": "text"
}

---

## Billing

POST /billing/checkout
Body:
{
  "plan": "creator"
}

POST /billing/webhook
Stripe webhook endpoint.
