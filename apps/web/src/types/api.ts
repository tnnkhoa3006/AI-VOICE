export type JobStatus = "queued" | "processing" | "completed" | "failed" | "cancelled";

export type Project = {
  id: string;
  title: string;
  type: string;
  status: string;
  created_at: string;
  updated_at: string;
};

export type GenerationJob = {
  id: string;
  status: JobStatus;
  output_audio_url: string | null;
  error_message: string | null;
};

export type TTSGenerateBody = {
  project_id: string;
  segment_id?: string;
  text: string;
  voice_name: string;
  style_prompt?: string;
  format: "wav" | "mp3";
};

