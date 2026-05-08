import { useState } from "react";

import { HumanReviewSection } from "../components/modeling/review/HumanReviewSection";
import { AITagsSection } from "../components/modeling/result/AITagsSection";
import { ResultPageBackground } from "../components/modeling/result/ResultPageBackground";
import { ResultPageHeader } from "../components/modeling/result/ResultPageHeader";
import { ResultViewTabs, type ResultView } from "../components/modeling/result/ResultViewTabs";
import { SteamEvidenceSection } from "../components/modeling/result/SteamEvidenceSection";
import { Button } from "../components/ui/button";
import { useModelingJobQuery } from "../hooks/modeling/useModelingJobQuery";
import type { ModelingRunResponse } from "../types/api";

type ModelingResultPageProps = {
  result: ModelingRunResponse;
  onCreateAnother: () => void;
};

export function ModelingResultPage({ result, onCreateAnother }: ModelingResultPageProps) {
  const [activeView, setActiveView] = useState<ResultView>("steam-evidence");
  const modelingJobQuery = useModelingJobQuery(result.job_id, result);
  const displayedResult = modelingJobQuery.data ?? result;

  return (
    <section className="relative -mx-6 -my-10 min-h-screen overflow-hidden bg-black px-6 py-10">
      <ResultPageBackground steamUrl={displayedResult.steam_url} />

      <div className="relative z-10 mx-auto grid min-h-[calc(100vh-80px)] max-w-6xl gap-10 py-24">
        <ResultPageHeader
          gameName={displayedResult.game_name}
          jobId={displayedResult.job_id}
          status={displayedResult.status}
        />
        <ResultViewTabs activeView={activeView} onViewChange={setActiveView} />

        {activeView === "steam-evidence" ? <SteamEvidenceSection result={displayedResult} /> : null}
        {activeView === "ai-tags" ? <AITagsSection result={displayedResult} /> : null}
        {activeView === "human-review" ? (
          <HumanReviewSection
            jobId={displayedResult.job_id}
            selectedTags={displayedResult.modeling_result?.selected_existing_tags ?? []}
          />
        ) : null}

        <div>
          <Button type="button" variant="quiet" onClick={onCreateAnother}>
            Create Another Job
          </Button>
        </div>
      </div>
    </section>
  );
}
