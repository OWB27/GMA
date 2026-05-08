import { useState } from "react";

import { submitReviewResult } from "../../lib/api";
import type { ReviewResultResponse, ReviewStatus, ReviewedTagInput } from "../../types/api";
import { Button } from "../ui/button";
import { HumanReviewExportActions } from "./HumanReviewExportActions";

type HumanReviewActionsProps = {
  jobId: string | null;
  reviewedTags: ReviewedTagInput[];
};

export function HumanReviewActions({ jobId, reviewedTags }: HumanReviewActionsProps) {
  const [reviewerNotes, setReviewerNotes] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submittedReview, setSubmittedReview] = useState<ReviewResultResponse | null>(null);

  async function handleSubmitReview(reviewStatus: ReviewStatus) {
    if (!jobId) {
      setSubmitError("Cannot submit review because this modeling result has no job id.");
      return;
    }

    setIsSubmitting(true);
    setSubmitError(null);

    try {
      const response = await submitReviewResult(jobId, {
        reviewed_tags: reviewedTags,
        review_status: reviewStatus,
        reviewer_notes: reviewerNotes.trim() || null,
      });
      setSubmittedReview(response);
    } catch (error) {
      setSubmittedReview(null);
      setSubmitError(error instanceof Error ? error.message : "Review request failed.");
    } finally {
      setIsSubmitting(false);
    }
  }

  const canExport = submittedReview?.review_status === "approved";

  return (
    <div>
      <label className="mt-8 grid gap-2">
        <span className="text-[0.68rem] font-bold uppercase tracking-[1.17px] text-[rgba(240,240,250,0.72)]">
          Reviewer Notes
        </span>
        <textarea
          className="min-h-28 w-full resize-y border-b border-[rgba(240,240,250,0.42)] bg-black/40 px-0 py-3 font-din text-base uppercase leading-6 tracking-[0.96px] text-[#f0f0fa] outline-none placeholder:text-[rgba(240,240,250,0.48)] focus:border-[#f0f0fa]"
          value={reviewerNotes}
          placeholder="Optional review notes"
          onChange={(event) => setReviewerNotes(event.target.value)}
        />
      </label>

      {submitError ? (
        <p className="mt-5 border-l border-[rgba(240,240,250,0.42)] pl-4 text-sm uppercase leading-6 text-[rgba(240,240,250,0.82)]">
          {submitError}
        </p>
      ) : null}

      {submittedReview ? (
        <p className="mt-5 border-l border-[rgba(240,240,250,0.42)] pl-4 text-sm uppercase leading-6 text-[rgba(240,240,250,0.82)]">
          Review saved as {submittedReview.review_status}.
        </p>
      ) : null}

      <div className="mt-8 flex flex-wrap gap-3">
        <Button
          type="button"
          disabled={isSubmitting || reviewedTags.length === 0}
          onClick={() => void handleSubmitReview("approved")}
        >
          Approve Review
        </Button>
        <Button
          type="button"
          variant="quiet"
          disabled={isSubmitting || reviewedTags.length === 0}
          onClick={() => void handleSubmitReview("rejected")}
        >
          Reject Review
        </Button>
      </div>

      {canExport ? <HumanReviewExportActions jobId={jobId} /> : null}
    </div>
  );
}
