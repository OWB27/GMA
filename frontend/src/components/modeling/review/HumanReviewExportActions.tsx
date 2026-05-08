import { useState } from "react";

import { useExportGRSPayloadMutation } from "../../../hooks/review/useExportGRSPayloadMutation";
import { Button } from "../../ui/button";

type HumanReviewExportActionsProps = {
  jobId: string | null;
};

export function HumanReviewExportActions({ jobId }: HumanReviewExportActionsProps) {
  const [missingJobIdError, setMissingJobIdError] = useState<string | null>(null);
  const exportMutation = useExportGRSPayloadMutation();

  function handleExport() {
    if (!jobId) {
      setMissingJobIdError("Cannot export because this modeling result has no job id.");
      return;
    }

    setMissingJobIdError(null);
    exportMutation.mutate({ jobId });
  }

  const exportError =
    missingJobIdError ?? (exportMutation.error instanceof Error ? exportMutation.error.message : null);
  const exportPayload = exportMutation.data ?? null;

  return (
    <>
      {exportError ? (
        <p className="mt-5 border-l border-[rgba(240,240,250,0.42)] pl-4 text-sm uppercase leading-6 text-[rgba(240,240,250,0.82)]">
          {exportError}
        </p>
      ) : null}

      <div className="mt-8">
        <Button type="button" variant="quiet" disabled={exportMutation.isPending} onClick={handleExport}>
          Export GRS Payload
        </Button>
      </div>

      {exportPayload ? (
        <pre className="mt-6 overflow-x-auto border-l border-[rgba(240,240,250,0.42)] bg-black/40 p-4 font-mono text-xs leading-5 text-[rgba(240,240,250,0.82)]">
          {JSON.stringify(exportPayload, null, 2)}
        </pre>
      ) : null}
    </>
  );
}
