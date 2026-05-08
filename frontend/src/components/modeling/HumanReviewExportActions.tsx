import { useState } from "react";

import { exportGRSPayload } from "../../lib/api";
import type { GRSExportPayload } from "../../types/api";
import { Button } from "../ui/button";

type HumanReviewExportActionsProps = {
  jobId: string | null;
};

export function HumanReviewExportActions({ jobId }: HumanReviewExportActionsProps) {
  const [isExporting, setIsExporting] = useState(false);
  const [exportError, setExportError] = useState<string | null>(null);
  const [exportPayload, setExportPayload] = useState<GRSExportPayload | null>(null);

  async function handleExport() {
    if (!jobId) {
      setExportError("Cannot export because this modeling result has no job id.");
      return;
    }

    setIsExporting(true);
    setExportError(null);

    try {
      const response = await exportGRSPayload(jobId);
      setExportPayload(response);
    } catch (error) {
      setExportPayload(null);
      setExportError(error instanceof Error ? error.message : "Export request failed.");
    } finally {
      setIsExporting(false);
    }
  }

  return (
    <>
      {exportError ? (
        <p className="mt-5 border-l border-[rgba(240,240,250,0.42)] pl-4 text-sm uppercase leading-6 text-[rgba(240,240,250,0.82)]">
          {exportError}
        </p>
      ) : null}

      <div className="mt-8">
        <Button type="button" variant="quiet" disabled={isExporting} onClick={() => void handleExport()}>
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
