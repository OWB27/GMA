import { useState } from "react";

import { AITagsSection } from "../components/modeling/AITagsSection";
import { SteamEvidenceSection } from "../components/modeling/SteamEvidenceSection";
import { Button } from "../components/ui/button";
import type { ModelingRunResponse } from "../types/api";

type ModelingResultPageProps = {
  result: ModelingRunResponse;
  onCreateAnother: () => void;
};

type ResultView = "steam-evidence" | "ai-tags";

function extractSteamAppId(steamUrl: string) {
  const match = steamUrl.match(/store\.steampowered\.com\/app\/(\d+)/);
  return match?.[1] ?? null;
}

function getSteamHeroImageUrl(steamUrl: string) {
  const appId = extractSteamAppId(steamUrl);
  if (!appId) {
    return null;
  }
  return `https://cdn.akamai.steamstatic.com/steam/apps/${appId}/library_hero.jpg`;
}

export function ModelingResultPage({ result, onCreateAnother }: ModelingResultPageProps) {
  const [activeView, setActiveView] = useState<ResultView>("steam-evidence");
  const heroImageUrl = getSteamHeroImageUrl(result.steam_url);

  return (
    <section className="relative -mx-6 -my-10 min-h-screen overflow-hidden bg-black px-6 py-10">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_42%,#121923_0%,#05070b_42%,#000_100%)]" />
      <div className="absolute inset-0 opacity-90 [background-image:radial-gradient(circle,rgba(240,240,250,0.92)_0_1px,transparent_1.6px),radial-gradient(circle,rgba(240,240,250,0.5)_0_1px,transparent_1.8px),radial-gradient(circle,rgba(240,240,250,0.34)_0_1px,transparent_2px)] [background-position:18px_28px,82px_128px,150px_64px] [background-size:180px_180px,260px_260px,340px_340px]" />
      <div className="absolute inset-0 opacity-55 [background-image:radial-gradient(circle,rgba(240,240,250,0.78)_0_1.2px,transparent_2px)] [background-position:40px_80px] [background-size:420px_420px]" />
      <div className="absolute left-1/2 top-1/2 h-[90vw] max-h-[980px] w-[90vw] max-w-[980px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-[rgba(240,240,250,0.16)]" />
      <div className="absolute left-1/2 top-1/2 h-[58vw] max-h-[640px] w-[58vw] max-w-[640px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-[rgba(240,240,250,0.1)]" />

      {heroImageUrl ? (
        <div
          className="absolute inset-x-0 top-20 h-[52vh] bg-top bg-no-repeat opacity-95 [background-size:100vw_auto] sm:[background-size:112vw_auto] md:top-0 md:h-[145vh] md:bg-center md:[background-size:auto_clamp(620px,72vw,1120px)]"
          style={{ backgroundImage: `url(${heroImageUrl})` }}
        />
      ) : null}
      <div className="absolute inset-0 bg-[linear-gradient(90deg,rgba(0,0,0,0.94),rgba(0,0,0,0.66)_46%,rgba(0,0,0,0.48)_100%)]" />
      <div className="absolute inset-x-0 bottom-0 h-48 bg-gradient-to-t from-black to-transparent" />

      <div className="relative z-10 mx-auto grid min-h-[calc(100vh-80px)] max-w-6xl gap-10 py-24">
        <header className="grid gap-6 md:grid-cols-[1fr_auto] md:items-end">
          <div>
            <p className="mb-3 text-[0.81rem] font-bold uppercase leading-none tracking-[1.17px]">
              Modeling Result
            </p>
            <h1 className="max-w-3xl text-5xl font-bold uppercase leading-none tracking-[0.96px] md:text-6xl">
              {result.game_name}
            </h1>
          </div>
          <div className="grid gap-3 border-t border-[rgba(240,240,250,0.24)] pt-5 text-sm uppercase leading-6 text-[rgba(240,240,250,0.78)] md:min-w-80">
            <div>
              <dt className="font-bold text-[#f0f0fa]">Status</dt>
              <dd className="m-0 break-words">{result.status}</dd>
            </div>
            <div>
              <dt className="font-bold text-[#f0f0fa]">Job ID</dt>
              <dd className="m-0 break-words">{result.job_id ?? "-"}</dd>
            </div>
          </div>
        </header>

        <div className="flex flex-wrap gap-3 border-b border-[rgba(240,240,250,0.24)] pb-5">
          <Button
            type="button"
            variant={activeView === "steam-evidence" ? "ghost" : "quiet"}
            onClick={() => setActiveView("steam-evidence")}
          >
            Steam Evidence
          </Button>
          <Button
            type="button"
            variant={activeView === "ai-tags" ? "ghost" : "quiet"}
            onClick={() => setActiveView("ai-tags")}
          >
            AI Tags
          </Button>
        </div>

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
