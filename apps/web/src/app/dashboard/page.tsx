import Link from "next/link";
import { Clock, FolderPlus, Headphones, MoreHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";

const projects = [
  {
    id: "new",
    title: "TikTok Ads Voice",
    type: "quick_tts",
    status: "active",
    updated: "Today"
  },
  {
    id: "story-demo",
    title: "Story Narration",
    type: "story",
    status: "draft",
    updated: "Yesterday"
  }
];

export default function DashboardPage() {
  return (
    <main className="min-h-screen bg-paper">
      <div className="mx-auto max-w-7xl px-5 py-6">
        <div className="mb-6 flex flex-col justify-between gap-4 border-b border-line pb-5 md:flex-row md:items-center">
          <div>
            <p className="text-sm font-semibold text-moss">Dashboard</p>
            <h1 className="text-3xl font-black tracking-normal">Voice projects</h1>
          </div>
          <Link href="/studio/new">
            <Button>
              <FolderPlus className="h-4 w-4" />
              New Project
            </Button>
          </Link>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          {projects.map((project) => (
            <Link
              href={`/studio/${project.id}`}
              key={project.id}
              className="rounded-lg border border-line bg-panel p-5 shadow-panel transition hover:border-moss"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-start gap-3">
                  <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-md bg-moss text-white">
                    <Headphones className="h-5 w-5" />
                  </div>
                  <div>
                    <h2 className="text-lg font-bold">{project.title}</h2>
                    <p className="mt-1 text-sm text-neutral-600">{project.type}</p>
                  </div>
                </div>
                <Button size="icon" variant="ghost" aria-label="Project menu">
                  <MoreHorizontal className="h-4 w-4" />
                </Button>
              </div>
              <div className="mt-5 flex items-center justify-between text-sm">
                <span className="rounded-md bg-white px-2 py-1 font-semibold text-moss">
                  {project.status}
                </span>
                <span className="inline-flex items-center gap-2 text-neutral-600">
                  <Clock className="h-4 w-4" />
                  {project.updated}
                </span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}

