import type { ModelingRunResponse, ReviewResultRequest, ReviewResultResponse } from "../types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

async function requestJson<T>(path: string, init: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...init.headers,
    },
    ...init,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function runModelingJob(gameName: string, steamUrl: string) {
  return requestJson<ModelingRunResponse>("/modeling-jobs/run", {
    method: "POST",
    body: JSON.stringify({
      game_name: gameName,
      steam_url: steamUrl,
    }),
  });
}

export function submitReviewResult(jobId: string, request: ReviewResultRequest) {
  return requestJson<ReviewResultResponse>(`/modeling-jobs/${jobId}/review`, {
    method: "POST",
    body: JSON.stringify(request),
  });
}
