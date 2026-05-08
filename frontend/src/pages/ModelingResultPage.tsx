import { useState } from "react";

import { AITagsSection } from "../components/modeling/AITagsSection";
import { ResultPageBackground } from "../components/modeling/ResultPageBackground";
import { ResultPageHeader } from "../components/modeling/ResultPageHeader";
import { ResultViewTabs, type ResultView } from "../components/modeling/ResultViewTabs";
import { SteamEvidenceSection } from "../components/modeling/SteamEvidenceSection";
import { Button } from "../components/ui/button";
import type { ModelingRunResponse } from "../types/api";

type ModelingResultPageProps = {
  result: ModelingRunResponse;
  onCreateAnother: () => void;
};

export function ModelingResultPage({ result, onCreateAnother }: ModelingResultPageProps) {
  const [activeView, setActiveView] = useState<ResultView>("steam-evidence");

  return (
    <section className="relative -mx-6 -my-10 min-h-screen overflow-hidden bg-black px-6 py-10">
      <ResultPageBackground steamUrl={result.steam_url} />

      <div className="relative z-10 mx-auto grid min-h-[calc(100vh-80px)] max-w-6xl gap-10 py-24">
        <ResultPageHeader gameName={result.game_name} jobId={result.job_id} status={result.status} />
        <ResultViewTabs activeView={activeView} onViewChange={setActiveView} />

        {activeView === "steam-evidence" ? <SteamEvidenceSection result={result} /> : null}
        {activeView === "ai-tags" ? <AITagsSection result={result} /> : null}

        <div>
          <Button type="button" variant="quiet" onClick={onCreateAnother}>
            Create Another Job
          </Button>
        </div>
      </div>
    </section>
  );
}
