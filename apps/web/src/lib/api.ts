import type { GenerationJob, Project, TTSGenerateBody } from "@/types/api";

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      "X-Dev-User-Email": "demo@mimostudio.local",
      ...init?.headers
    }
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? `Request failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function listProjects() {
  return apiRequest<Project[]>("/projects");
}

export function createProject(title: string) {
  return apiRequest<Project>("/projects", {
    method: "POST",
    body: JSON.stringify({ title, type: "quick_tts" })
  });
}

export function generatePreview(body: Omit<TTSGenerateBody, "segment_id">) {
  return apiRequest<{ job_id: string; status: string }>("/tts/preview", {
    method: "POST",
    body: JSON.stringify(body)
  });
}

export function generateFullAudio(body: TTSGenerateBody) {
  return apiRequest<{ job_id: string; status: string }>("/tts/generate", {
    method: "POST",
    body: JSON.stringify(body)
  });
}

export function getTTSJob(jobId: string) {
  return apiRequest<GenerationJob>(`/tts/jobs/${jobId}`);
}

