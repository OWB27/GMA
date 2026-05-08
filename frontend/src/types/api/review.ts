import type { LocalizedText } from "./modeling";

export type ReviewStatus = "approved" | "rejected";

export type ReviewedTagInput = {
  tag_code: string;
  weight: number;
  confidence?: number | null;
  evidence_snippets: LocalizedText[];
  reason?: LocalizedText | null;
};

export type ReviewResultRequest = {
  reviewed_tags: ReviewedTagInput[];
  review_status: ReviewStatus;
  reviewer_notes?: string | null;
};

export type ReviewResultResponse = {
  job_id: string;
  review_status: ReviewStatus;
  reviewed_tags: ReviewedTagInput[];
  reviewer_notes?: string | null;
};
