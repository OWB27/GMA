import { useEffect, useState } from "react";

type ResultPageBackgroundProps = {
  steamUrl: string;
};

function extractSteamAppId(steamUrl: string) {
  const match = steamUrl.match(/store\.steampowered\.com\/app\/(\d+)/);
  return match?.[1] ?? null;
}

function buildSteamBackgroundCandidates(steamUrl: string) {
  const appId = extractSteamAppId(steamUrl);
  if (!appId) {
    return [];
  }

  return [
    `https://cdn.akamai.steamstatic.com/steam/apps/${appId}/library_hero_2x.jpg`,
    `https://cdn.akamai.steamstatic.com/steam/apps/${appId}/library_hero.jpg`,
  ];
}

export function ResultPageBackground({ steamUrl }: ResultPageBackgroundProps) {
  const [backgroundCandidateIndex, setBackgroundCandidateIndex] = useState(0);
  const heroImageCandidates = buildSteamBackgroundCandidates(steamUrl);
  const heroImageUrl = heroImageCandidates[backgroundCandidateIndex] ?? null;

  useEffect(() => {
    setBackgroundCandidateIndex(0);
  }, [steamUrl]);

  function handleHeroImageError() {
    setBackgroundCandidateIndex((currentIndex) => {
      const nextIndex = currentIndex + 1;
      return nextIndex < heroImageCandidates.length ? nextIndex : currentIndex;
    });
  }

  return (
    <>
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_42%,#121923_0%,#05070b_42%,#000_100%)]" />
      <div className="absolute inset-0 opacity-90 [background-image:radial-gradient(circle,rgba(240,240,250,0.92)_0_1px,transparent_1.6px),radial-gradient(circle,rgba(240,240,250,0.5)_0_1px,transparent_1.8px),radial-gradient(circle,rgba(240,240,250,0.34)_0_1px,transparent_2px)] [background-position:18px_28px,82px_128px,150px_64px] [background-size:180px_180px,260px_260px,340px_340px]" />
      <div className="absolute inset-0 opacity-55 [background-image:radial-gradient(circle,rgba(240,240,250,0.78)_0_1.2px,transparent_2px)] [background-position:40px_80px] [background-size:420px_420px]" />
      <div className="absolute left-1/2 top-1/2 h-[90vw] max-h-[980px] w-[90vw] max-w-[980px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-[rgba(240,240,250,0.16)]" />
      <div className="absolute left-1/2 top-1/2 h-[58vw] max-h-[640px] w-[58vw] max-w-[640px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-[rgba(240,240,250,0.1)]" />

      {heroImageUrl ? (
        <>
          <img
            alt=""
            aria-hidden="true"
            className="hidden"
            src={heroImageUrl}
            onError={handleHeroImageError}
          />
          <div
            className="absolute inset-x-0 top-20 h-[52vh] bg-top bg-no-repeat opacity-95 [background-size:100vw_auto] sm:[background-size:112vw_auto] md:top-0 md:h-[145vh] md:bg-center md:[background-size:auto_clamp(620px,72vw,1120px)]"
            style={{ backgroundImage: `url(${heroImageUrl})` }}
          />
        </>
      ) : null}

      <div className="absolute inset-0 bg-[linear-gradient(90deg,rgba(0,0,0,0.94),rgba(0,0,0,0.66)_46%,rgba(0,0,0,0.48)_100%)]" />
      <div className="absolute inset-x-0 bottom-0 h-48 bg-gradient-to-t from-black to-transparent" />
    </>
  );
}
