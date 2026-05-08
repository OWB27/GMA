import { useMutation } from "@tanstack/react-query";

import { exportGRSPayload } from "../../lib/api";

type ExportGRSPayloadVariables = {
  jobId: string;
};

export function useExportGRSPayloadMutation() {
  return useMutation({
    mutationFn: ({ jobId }: ExportGRSPayloadVariables) => exportGRSPayload(jobId),
  });
}
