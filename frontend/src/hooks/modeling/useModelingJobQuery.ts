import { useQuery } from "@tanstack/react-query";

import { getModelingJob } from "../../lib/api";
import type { ModelingRunResponse } from "../../types/api";

export function useModelingJobQuery(jobId: string | null, initialData?: ModelingRunResponse) {
  return useQuery({
    queryKey: ["modelingJob", jobId],
    queryFn: () => getModelingJob(jobId as string),
    enabled: Boolean(jobId),
    initialData,
  });
}
