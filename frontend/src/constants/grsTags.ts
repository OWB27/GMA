export const GRS_TAG_CODES = [
  "story_rich",
  "character_growth",
  "open_world",
  "exploration",
  "fast_paced",
  "combat",
  "challenge",
  "competitive",
  "relaxed",
  "choices_matter",
  "immersive",
  "strategy",
  "resource_management",
  "build_variety",
  "replayable",
  "cozy",
  "puzzle_solving",
  "survival",
  "social_sim",
  "horror_tension",
] as const;

export type GrsTagCode = (typeof GRS_TAG_CODES)[number];
