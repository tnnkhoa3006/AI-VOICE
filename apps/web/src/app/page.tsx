import Link from "next/link";
import { ArrowRight, AudioLines, Download, FolderPlus, Play, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

const steps = [
  "Idea",
  "AI script",
  "Segments",
  "Voice",
  "MiMo job",
  "Audio"
];

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <header className="border-b border-line bg-panel/80">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-md bg-ink text-white">
              <AudioLines className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm font-bold">MiMo Voice Studio</p>
              <p className="text-xs text-neutral-600">AI voice-over workspace</p>
            </div>
          </div>
          <Link href="/dashboard">
            <Button variant="secondary" size="sm">
              <FolderPlus className="h-4 w-4" />
              Dashboard
            </Button>
          </Link>
        </div>
      </header>

      <section className="mx-auto grid min-h-[calc(100vh-73px)] max-w-7xl grid-cols-1 gap-8 px-5 py-8 lg:grid-cols-[0.86fr_1.14fr] lg:items-center">
        <div className="max-w-2xl">
          <p className="mb-3 inline-flex items-center gap-2 rounded-md border border-line bg-panel px-3 py-1 text-sm font-semibold text-moss">
            <Sparkles className="h-4 w-4" />
            Studio first, converter second
          </p>
          <h1 className="text-4xl font-black leading-tight tracking-normal text-ink md:text-6xl">
            MiMo Voice Studio
          </h1>
          <p className="mt-5 max-w-xl text-lg leading-8 text-neutral-700">
            Turn a rough idea into a polished voice-over project with script rewriting,
            segment editing, voice style, queued generation, and downloadable audio.
          </p>
          <div className="mt-7 flex flex-wrap gap-3">
            <Link href="/studio/new">
              <Button>
                <Play className="h-4 w-4" />
                Open Studio
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button variant="secondary">
                <ArrowRight className="h-4 w-4" />
                View Projects
              </Button>
            </Link>
          </div>
          <div className="mt-8 grid grid-cols-3 gap-3 text-sm sm:grid-cols-6">
            {steps.map((step) => (
              <div key={step} className="rounded-md border border-line bg-panel px-3 py-3 font-semibold">
                {step}
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-lg border border-line bg-panel p-4 shadow-panel">
          <div className="grid gap-4 lg:grid-cols-[1fr_240px]">
            <div className="rounded-md border border-line bg-white p-4">
              <div className="mb-4 flex items-center justify-between">
                <div>
                  <p className="text-sm font-bold">Ad Voice Project</p>
                  <p className="text-xs text-neutral-500">3 segments, warm narration</p>
                </div>
                <Button size="icon" variant="secondary" aria-label="Download">
                  <Download className="h-4 w-4" />
                </Button>
              </div>
              <div className="space-y-3">
                {[0, 1, 2].map((item) => (
                  <div key={item} className="rounded-md border border-line bg-paper p-3">
                    <div className="mb-3 flex items-center justify-between gap-3">
                      <span className="text-xs font-bold uppercase text-neutral-500">
                        Segment {item + 1}
                      </span>
                      <span className="rounded-md bg-moss px-2 py-1 text-xs font-bold text-white">
                        completed
                      </span>
                    </div>
                    <div className="flex h-16 items-end gap-1">
                      {Array.from({ length: 32 }).map((_, index) => (
                        <span
                          key={index}
                          className="waveform-bar w-full rounded-sm bg-coral"
                          style={{ height: `${22 + ((index * 17 + item * 9) % 38)}px` }}
                        />
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-md border border-line bg-ink p-4 text-white">
              <p className="text-sm font-bold">Generation Queue</p>
              <div className="mt-5 space-y-4">
                <QueueRow label="Preview" value="done" />
                <QueueRow label="Full audio" value="processing" />
                <QueueRow label="Storage" value="next" />
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

function QueueRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between border-b border-white/15 pb-3 text-sm">
      <span>{label}</span>
      <span className="font-semibold text-[#f2c879]">{value}</span>
    </div>
  );
}

