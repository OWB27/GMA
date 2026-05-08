import { useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";

import { HumanReviewSection } from "../components/modeling/review/HumanReviewSection";
import { AITagsSection } from "../components/modeling/result/AITagsSection";
import { ResultPageBackground } from "../components/modeling/result/ResultPageBackground";
import { ResultPageHeader } from "../components/modeling/result/ResultPageHeader";
import { ResultViewTabs, type ResultView } from "../components/modeling/result/ResultViewTabs";
import { SteamEvidenceSection } from "../components/modeling/result/SteamEvidenceSection";
import { Button } from "../components/ui/button";
import { useModelingJobQuery } from "../hooks/modeling/useModelingJobQuery";
import { getErrorMessage } from "../lib/errors";
import type { ModelingRunResponse } from "../types/api";

type ModelingResultLocationState = {
  initialResult?: ModelingRunResponse;
};

export function ModelingResultPage() {
  const navigate = useNavigate();
  const { jobId } = useParams();
  const location = useLocation();
  const [activeView, setActiveView] = useState<ResultView>("steam-evidence");
  const initialResult = (location.state as ModelingResultLocationState | null)?.initialResult;
  const modelingJobQuery = useModelingJobQuery(jobId ?? null, initialResult);
  const displayedResult = modelingJobQuery.data;

  if (!jobId) {
    return <ResultPageStatus message="Missing modeling job id." onCreateAnother={() => navigate("/")} />;
  }

  if (modelingJobQuery.isLoading) {
    return <ResultPageStatus message="Loading modeling job..." onCreateAnother={() => navigate("/")} />;
  }

  if (modelingJobQuery.isError || !displayedResult) {
    const message = modelingJobQuery.error ? getErrorMessage(modelingJobQuery.error) : "Modeling job could not be loaded.";
    return <ResultPageStatus message={message} onCreateAnother={() => navigate("/")} />;
  }

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
          <Button type="button" variant="quiet" onClick={() => navigate("/")}>
            Create Another Job
          </Button>
        </div>
      </div>
    </section>
  );
}

type ResultPageStatusProps = {
  message: string;
  onCreateAnother: () => void;
};

function ResultPageStatus({ message, onCreateAnother }: ResultPageStatusProps) {
  return (
    <section className="mx-auto grid min-h-[calc(100vh-80px)] max-w-4xl content-center gap-8">
      <div>
        <p className="mb-3 text-[0.81rem] font-bold uppercase leading-none tracking-[1.17px]">Modeling Job</p>
        <h1 className="text-4xl font-bold uppercase leading-none tracking-[0.96px] md:text-5xl">{message}</h1>
      </div>
      <div>
        <Button type="button" variant="quiet" onClick={onCreateAnother}>
          Create Another Job
        </Button>
      </div>
    </section>
  );
}
