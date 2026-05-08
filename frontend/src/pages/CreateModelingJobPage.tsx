import { type FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";

import { CreatePageBackground } from "../components/modeling/create/CreatePageBackground";
import { CreateModelingJobForm, type ModelingJobForm } from "../components/modeling/create/CreateModelingJobForm";
import { ModelingRunNotice } from "../components/modeling/create/ModelingRunNotice";
import { useRunModelingJobMutation } from "../hooks/modeling/useRunModelingJobMutation";
import { getErrorMessage } from "../lib/errors";
import type { ModelingRunResponse } from "../types/api";

export function CreateModelingJobPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState<ModelingJobForm>({
    gameName: "",
    steamUrl: "",
  });
  const runModelingMutation = useRunModelingJobMutation();

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    runModelingMutation.mutate(
      {
        gameName: form.gameName,
        steamUrl: form.steamUrl,
      },
      {
        onSuccess: (result: ModelingRunResponse) => {
          if (result.job_id) {
            navigate(`/jobs/${result.job_id}`, { state: { initialResult: result } });
          }
        },
      },
    );
  }

  function handleReset() {
    setForm({
      gameName: "",
      steamUrl: "",
    });
    runModelingMutation.reset();
  }

  const errorMessage = runModelingMutation.error ? getErrorMessage(runModelingMutation.error) : null;

  return (
    <section className="relative -mx-6 -my-10 min-h-screen overflow-hidden bg-black px-6 py-10">
      <CreatePageBackground />

      <div className="relative z-10 mx-auto grid min-h-[calc(100vh-80px)] max-w-6xl items-end gap-12 md:grid-cols-[1.1fr_0.9fr]">
        <div>
          <p className="mb-3 text-[0.81rem] font-bold uppercase leading-none tracking-[1.17px]">
            Game Modeling Agent
          </p>
          <h1 className="max-w-3xl text-5xl font-bold uppercase leading-none tracking-[0.96px] md:text-6xl">
            GMA Frontend Controls
          </h1>
          <p className="mt-6 max-w-2xl text-base uppercase leading-7 text-[rgba(240,240,250,0.82)]">
            Create a Steam-based modeling job, then review the AI draft before exporting GRS-compatible tags.
          </p>
        </div>

        <div className="grid gap-5">
          <CreateModelingJobForm
            form={form}
            isRunning={runModelingMutation.isPending}
            onFormChange={setForm}
            onReset={handleReset}
            onSubmit={handleSubmit}
          />
          <ModelingRunNotice errorMessage={errorMessage} />
        </div>
      </div>
    </section>
  );
}
