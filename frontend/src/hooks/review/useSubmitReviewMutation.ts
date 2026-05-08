import { useMutation } from "@tanstack/react-query";

import { submitReviewResult } from "../../lib/api";
import type { ReviewResultRequest } from "../../types/api";

type SubmitReviewVariables = {
  jobId: string;
  request: ReviewResultRequest;
};

export function useSubmitReviewMutation() {
  return useMutation({
    mutationFn: ({ jobId, request }: SubmitReviewVariables) => submitReviewResult(jobId, request),
  });
}
