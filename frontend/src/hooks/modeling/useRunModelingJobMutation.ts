import { useMutation } from "@tanstack/react-query";

import { runModelingJob } from "../../lib/api";

type RunModelingJobVariables = {
  gameName: string;
  steamUrl: string;
};

export function useRunModelingJobMutation() {
  return useMutation({
    mutationFn: ({ gameName, steamUrl }: RunModelingJobVariables) => runModelingJob(gameName, steamUrl),
  });
}
