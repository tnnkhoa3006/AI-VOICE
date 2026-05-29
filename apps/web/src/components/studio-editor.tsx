"use client";

import { useEffect, useMemo, useState } from "react";
import { Download, Loader2, Play, Save, Wand2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { createProject, generateFullAudio, generatePreview, getTTSJob } from "@/lib/api";
import type { GenerationJob } from "@/types/api";

const voices = ["mimo_default", "Mia", "Chloe", "Milo", "Dean"];

export function StudioEditor({ projectId }: { projectId: string }) {
  const [activeProjectId, setActiveProjectId] = useState(projectId);
  const [text, setText] = useState("Start with a sharp hook, explain the product benefit, then close with a direct call to action.");
  const [voice, setVoice] = useState("Mia");
  const [stylePrompt, setStylePrompt] = useState("Warm, natural, confident, clear pacing");
  const [format, setFormat] = useState<"wav" | "mp3">("wav");
  const [jobId, setJobId] = useState<string | null>(null);
  const [job, setJob] = useState<GenerationJob | null>(null);
  const [error, setError] = useState<string | null>(null);

  const canGenerate = text.trim().length > 0;
  const isWorking = job?.status === "queued" || job?.status === "processing";
  const creditEstimate = useMemo(() => Math.max(1, Math.ceil(text.length / 100)), [text]);

  useEffect(() => {
    if (!jobId) return;

    const interval = window.setInterval(async () => {
      try {
        const nextJob = await getTTSJob(jobId);
        setJob(nextJob);
        if (nextJob.status === "completed" || nextJob.status === "failed") {
          window.clearInterval(interval);
        }
      } catch (pollError) {
        setError(pollError instanceof Error ? pollError.message : "Unable to poll job");
        window.clearInterval(interval);
      }
    }, 1800);

    return () => window.clearInterval(interval);
  }, [jobId]);

  async function resolveProjectId() {
    if (activeProjectId !== "new") return activeProjectId;

    const project = await createProject("Untitled Voice Project");
    setActiveProjectId(project.id);
    return project.id;
  }

  async function startPreview() {
    setError(null);
    setJob(null);
    try {
      const targetProjectId = await resolveProjectId();
      const queued = await generatePreview({
        project_id: targetProjectId,
        text,
        voice_name: voice,
        style_prompt: stylePrompt,
        format
      });
      setJobId(queued.job_id);
      setJob({ id: queued.job_id, status: "queued", output_audio_url: null, error_message: null });
    } catch (previewError) {
      setError(previewError instanceof Error ? previewError.message : "Preview failed");
    }
  }

  async function startFullGenerate() {
    setError(null);
    setJob(null);
    try {
      const targetProjectId = await resolveProjectId();
      const queued = await generateFullAudio({
        project_id: targetProjectId,
        text,
        voice_name: voice,
        style_prompt: stylePrompt,
        format
      });
      setJobId(queued.job_id);
      setJob({ id: queued.job_id, status: "queued", output_audio_url: null, error_message: null });
    } catch (generateError) {
      setError(generateError instanceof Error ? generateError.message : "Generation failed");
    }
  }

  return (
    <main className="min-h-screen bg-paper">
      <div className="mx-auto grid max-w-7xl gap-5 px-5 py-5 lg:grid-cols-[280px_1fr_320px]">
        <aside className="rounded-lg border border-line bg-panel p-4 shadow-panel">
          <div className="mb-5 flex items-center justify-between">
            <h1 className="text-lg font-black">Studio</h1>
            <Button size="icon" variant="secondary" aria-label="Save project">
              <Save className="h-4 w-4" />
            </Button>
          </div>
          <div className="space-y-3">
            {["Script", "Segments", "Voice", "Audio"].map((item, index) => (
              <div
                className="rounded-md border border-line bg-white px-3 py-3 text-sm font-semibold"
                key={item}
              >
                {index + 1}. {item}
              </div>
            ))}
          </div>
        </aside>

        <section className="rounded-lg border border-line bg-panel p-4 shadow-panel">
          <div className="mb-4 flex flex-col justify-between gap-3 border-b border-line pb-4 md:flex-row md:items-center">
            <div>
              <p className="text-sm font-semibold text-moss">Project {activeProjectId}</p>
              <h2 className="text-2xl font-black tracking-normal">Script editor</h2>
            </div>
            <Button variant="secondary">
              <Wand2 className="h-4 w-4" />
              Rewrite
            </Button>
          </div>

          <textarea
            className="min-h-[320px] w-full resize-y rounded-md border border-line bg-white p-4 text-base leading-7 outline-none focus:border-moss"
            value={text}
            onChange={(event) => setText(event.target.value)}
          />

          <div className="mt-4 grid gap-3 md:grid-cols-3">
            <label className="text-sm font-semibold">
              Voice
              <select
                className="mt-2 h-10 w-full rounded-md border border-line bg-white px-3"
                value={voice}
                onChange={(event) => setVoice(event.target.value)}
              >
                {voices.map((voiceName) => (
                  <option key={voiceName} value={voiceName}>
                    {voiceName}
                  </option>
                ))}
              </select>
            </label>

            <label className="text-sm font-semibold md:col-span-2">
              Style prompt
              <input
                className="mt-2 h-10 w-full rounded-md border border-line bg-white px-3"
                value={stylePrompt}
                onChange={(event) => setStylePrompt(event.target.value)}
              />
            </label>
          </div>
        </section>

        <aside className="rounded-lg border border-line bg-panel p-4 shadow-panel">
          <h2 className="text-lg font-black">Generate</h2>
          <div className="mt-4 grid grid-cols-2 gap-2">
            {(["wav", "mp3"] as const).map((item) => (
              <button
                className={`h-10 rounded-md border text-sm font-bold ${
                  format === item
                    ? "border-moss bg-moss text-white"
                    : "border-line bg-white text-ink"
                }`}
                key={item}
                onClick={() => setFormat(item)}
                type="button"
              >
                {item.toUpperCase()}
              </button>
            ))}
          </div>

          <div className="mt-5 rounded-md border border-line bg-white p-4">
            <p className="text-sm font-semibold text-neutral-600">Estimated credits</p>
            <p className="mt-1 text-3xl font-black">{creditEstimate}</p>
          </div>

          <div className="mt-5 space-y-3">
            <Button className="w-full" disabled={!canGenerate || isWorking} onClick={startPreview}>
              {isWorking ? <Loader2 className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
              Preview
            </Button>
            <Button className="w-full" disabled={!canGenerate || isWorking} onClick={startFullGenerate} variant="secondary">
              {isWorking ? <Loader2 className="h-4 w-4 animate-spin" /> : <Download className="h-4 w-4" />}
              Full Audio
            </Button>
          </div>

          {job ? (
            <div className="mt-5 rounded-md border border-line bg-white p-4">
              <p className="text-sm font-semibold text-neutral-600">Job status</p>
              <p className="mt-1 text-lg font-black">{job.status}</p>
              {job.output_audio_url ? (
                <audio className="mt-3 w-full" controls src={job.output_audio_url} />
              ) : null}
              {job.error_message ? (
                <p className="mt-3 text-sm font-semibold text-coral">{job.error_message}</p>
              ) : null}
            </div>
          ) : null}

          {error ? (
            <p className="mt-4 rounded-md border border-coral bg-white p-3 text-sm font-semibold text-coral">
              {error}
            </p>
          ) : null}
        </aside>
      </div>
    </main>
  );
}
