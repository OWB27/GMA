import type { ModelingRunResponse } from "../../types/api";

type AITagsSectionProps = {
  result: ModelingRunResponse;
};

function formatPercent(value: number) {
  return `${Math.round(value * 100)}%`;
}

export function AITagsSection({ result }: AITagsSectionProps) {
  return (
    <section>
      <h2 className="mb-5 text-2xl font-bold uppercase tracking-[0.96px]">AI Tags</h2>
      <p className="mb-6 text-sm uppercase leading-6 text-[rgba(240,240,250,0.82)]">
        {result.modeling_result?.overall_summary ?? "No data"}
      </p>
      <div className="grid gap-5">
        {result.modeling_result?.selected_existing_tags.map((tag) => (
          <article className="border-b border-[rgba(240,240,250,0.24)] pb-5" key={tag.tag_code}>
            <div className="mb-3 flex flex-wrap items-baseline justify-between gap-3">
              <h3 className="text-sm font-bold uppercase tracking-[1.17px]">{tag.tag_code}</h3>
              <p className="text-xs uppercase tracking-[1px] text-[rgba(240,240,250,0.72)]">
                Weight {tag.suggested_weight} / Confidence {formatPercent(tag.confidence)}
              </p>
            </div>
            <p className="text-sm uppercase leading-6 text-[rgba(240,240,250,0.82)]">{tag.reason.en}</p>
            <p className="mt-3 text-xs uppercase leading-5 text-[rgba(240,240,250,0.68)]">
              Evidence: {tag.evidence_snippets.map((snippet) => snippet.en).join(" | ")}
            </p>
          </article>
        )) ?? <p className="text-sm uppercase leading-6 text-[rgba(240,240,250,0.82)]">No data</p>}
      </div>
    </section>
  );
}
