export type LocalizedText = {
  en: string;
  zh: string;
};

export type SourceBundle = {
  short_description?: string | null;
  detailed_description?: string | null;
  review_summary?: string | null;
  official_genres?: string[];
  official_categories?: string[];
  popular_user_tags?: string[];
  page_text?: string | null;
  source_urls?: string[];
  extraction_notes?: string | null;
};

export type SelectedTagSuggestion = {
  tag_code: string;
  suggested_weight: number;
  confidence: number;
  evidence_snippets: LocalizedText[];
  reason: LocalizedText;
};

export type ModelingResult = {
  overall_summary: string;
  selected_existing_tags: SelectedTagSuggestion[];
  warnings: string[];
};

export type ValidationResult = {
  is_valid?: boolean;
  errors?: string[];
  warnings?: string[];
};

export type TraceEvent = {
  node: string;
  message: string;
};

export type SourceAssessment = {
  is_sufficient: boolean;
  confidence: number;
  missing_information: string[];
  reason: string;
  recommended_action: "continue_modeling" | "fetch_supplemental_sources";
};

export type ModelingRunResponse = {
  job_id: string | null;
  game_name: string;
  steam_url: string;
  source_bundle: SourceBundle | null;
  source_assessment?: SourceAssessment | null;
  retrieved_context: unknown;
  modeling_result: ModelingResult | null;
  validation_result: ValidationResult | null;
  status: string;
  errors: string[];
  trace: TraceEvent[];
};
