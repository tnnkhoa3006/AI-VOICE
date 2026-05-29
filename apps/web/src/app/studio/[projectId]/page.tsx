import { StudioEditor } from "@/components/studio-editor";

export default async function StudioPage({
  params
}: {
  params: Promise<{ projectId: string }>;
}) {
  const { projectId } = await params;
  return <StudioEditor projectId={projectId} />;
}
