# 03 - Database Schema

## users
- id uuid pk
- email text unique
- name text
- avatar_url text nullable
- plan text default 'free'
- credit_balance integer default 0
- created_at timestamp
- updated_at timestamp

## projects
- id uuid pk
- user_id uuid fk users.id
- title text
- type text
  - quick_tts
  - script_voice
  - dialogue
  - story
  - elearning
- status text
  - active
  - archived
- created_at timestamp
- updated_at timestamp

## voice_profiles
- id uuid pk
- user_id uuid fk users.id nullable for built-in
- name text
- type text
  - built_in
  - voice_design
  - voice_clone
- provider text default 'mimo'
- provider_model text
- provider_voice text nullable
- design_prompt text nullable
- sample_audio_url text nullable
- consent_confirmed boolean default false
- created_at timestamp

## tts_segments
- id uuid pk
- project_id uuid fk projects.id
- order_index integer
- text text
- voice_profile_id uuid fk voice_profiles.id nullable
- voice_name text nullable
- style_prompt text nullable
- audio_url text nullable
- audio_format text
- duration_seconds numeric nullable
- status text
  - draft
  - queued
  - processing
  - completed
  - failed
- created_at timestamp
- updated_at timestamp

## generation_jobs
- id uuid pk
- user_id uuid fk users.id
- project_id uuid fk projects.id
- segment_id uuid fk tts_segments.id nullable
- provider text default 'mimo'
- model text
- input_text text
- style_prompt text nullable
- voice_payload jsonb nullable
- status text
  - queued
  - processing
  - completed
  - failed
  - cancelled
- reserved_credits integer
- used_credits integer nullable
- output_audio_url text nullable
- error_message text nullable
- retry_count integer default 0
- created_at timestamp
- started_at timestamp nullable
- completed_at timestamp nullable

## credit_transactions
- id uuid pk
- user_id uuid fk users.id
- amount integer
- type text
  - reserve
  - consume
  - refund
  - purchase
  - bonus
- reason text
- job_id uuid fk generation_jobs.id nullable
- created_at timestamp

## subscriptions
- id uuid pk
- user_id uuid fk users.id
- provider text
- provider_customer_id text
- provider_subscription_id text
- plan text
- status text
- current_period_start timestamp
- current_period_end timestamp
- created_at timestamp
- updated_at timestamp

## audio_assets
- id uuid pk
- user_id uuid fk users.id
- project_id uuid fk projects.id nullable
- segment_id uuid fk tts_segments.id nullable
- storage_key text
- public_url text nullable
- mime_type text
- size_bytes integer
- duration_seconds numeric nullable
- created_at timestamp

---

# Indexes
- users.email unique
- projects.user_id
- tts_segments.project_id, order_index
- generation_jobs.user_id, created_at
- generation_jobs.status
- audio_assets.user_id
- credit_transactions.user_id, created_at
