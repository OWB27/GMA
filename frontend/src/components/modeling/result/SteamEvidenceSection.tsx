import type { ModelingRunResponse } from "../../../types/api";
import { ResultBlock } from "./ResultBlock";

type SteamEvidenceSectionProps = {
  result: ModelingRunResponse;
};

function joinValues(values: string[] | undefined) {
  return values?.filter(Boolean).join(" / ") || "No data";
}

export function SteamEvidenceSection({ result }: SteamEvidenceSectionProps) {
  return (
    <section>
      <h2 className="mb-5 text-2xl font-bold uppercase tracking-[0.96px]">Steam Evidence</h2>
      <ResultBlock title="Official Description">
        {result.source_bundle?.short_description ?? "No data"}
      </ResultBlock>
      <ResultBlock title="Official Genres">
        {joinValues(result.source_bundle?.official_genres)}
      </ResultBlock>
      <ResultBlock title="Official Categories">
        {joinValues(result.source_bundle?.official_categories)}
      </ResultBlock>
      <ResultBlock title="Steam User Tags">
        {joinValues(result.source_bundle?.popular_user_tags)}
      </ResultBlock>
      <ResultBlock title="English Review Summary">
        {result.source_bundle?.review_summary ?? "No data"}
      </ResultBlock>
    </section>
  );
}
