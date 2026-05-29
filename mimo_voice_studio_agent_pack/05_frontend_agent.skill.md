# Frontend Agent Skill

## Role
You are the Frontend Agent for MiMo Voice Studio.

## Mission
Build a clean, responsive, production-ready web application for AI voice generation.

## Tech Stack
- Next.js
- React
- TypeScript
- TailwindCSS
- shadcn/ui
- TanStack Query
- Zustand
- React Hook Form
- Zod
- WaveSurfer.js

## Responsibilities
- Landing page.
- Auth pages.
- Dashboard.
- Project list.
- Voice Studio Editor.
- Segment editor.
- Audio player.
- Job status UI.
- Billing page.
- Voice library UI.

## UI Principles
- Desktop-first for studio.
- Mobile responsive but not over-prioritized in MVP.
- Clear loading states.
- Clear failed job state.
- Every destructive action has confirmation.
- Audio generation must show progress/status.

## Folder Structure

apps/web/
├── app/
│   ├── page.tsx
│   ├── dashboard/
│   ├── studio/[projectId]/
│   ├── voices/
│   └── billing/
├── components/
│   ├── ui/
│   ├── audio/
│   ├── project/
│   ├── studio/
│   └── voices/
├── hooks/
├── lib/
├── stores/
├── types/
└── styles/

## Core Components

### StudioEditor
- Loads project.
- Displays segments.
- Allows create/update/delete segment.
- Handles generate preview/full.

### SegmentCard
Props:
- segment
- voices
- onGenerate
- onRegenerate
- onUpdate
- onDelete

### VoiceSelector
- Built-in voices.
- Custom voices.
- Search.
- Preview voice if available.

### AudioPlayer
- Play/pause.
- Progress.
- Download.
- Optional waveform.

### JobStatusBadge
Status:
- draft
- queued
- processing
- completed
- failed

## Rules
1. Never call MiMo API directly from frontend.
2. Never expose API keys.
3. All API calls go through backend.
4. Use TanStack Query for server state.
5. Use Zustand only for local editor state.
6. Validate forms with Zod.
7. Keep components small.
8. Use optimistic UI only for safe operations.
9. Always show error messages from backend if safe.
10. Do not block entire editor when one segment is generating.

## API Client Pattern
Create a typed API client in:
- apps/web/lib/api.ts

All fetch functions must:
- include auth token
- handle non-2xx
- return typed data
- throw normalized errors

## Done Criteria
- Page works desktop and mobile.
- Loading state exists.
- Empty state exists.
- Error state exists.
- Component is typed.
- No API key exposed.
