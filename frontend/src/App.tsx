import { type FormEvent, useState } from "react";

import { CreateModelingJobForm, type ModelingJobForm } from "./components/modeling/create/CreateModelingJobForm";
import { ModelingRunNotice } from "./components/modeling/create/ModelingRunNotice";
import { useRunModelingJobMutation } from "./hooks/modeling/useRunModelingJobMutation";
import { ModelingResultPage } from "./pages/ModelingResultPage";
import type { ModelingRunResponse } from "./types/api";

export default function App() {
  const [form, setForm] = useState<ModelingJobForm>({
    gameName: "",
    steamUrl: "",
  });
  const [runResult, setRunResult] = useState<ModelingRunResponse | null>(null);
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
          setRunResult(result);
        },
        onError: () => {
          setRunResult(null);
        },
      },
    );
  }

  function handleReset() {
    setForm({
      gameName: "",
      steamUrl: "",
    });
    setRunResult(null);
    runModelingMutation.reset();
  }

  const errorMessage = runModelingMutation.error instanceof Error ? runModelingMutation.error.message : null;

  return (
    <main className="min-h-screen bg-black px-6 py-10 text-[#f0f0fa] font-din">
      {runResult ? (
        <ModelingResultPage result={runResult} onCreateAnother={handleReset} />
      ) : (
        <section className="mx-auto grid min-h-[calc(100vh-80px)] max-w-6xl items-end gap-12 md:grid-cols-[1.1fr_0.9fr]">
          <div>
            <p className="mb-3 text-[0.81rem] font-bold uppercase leading-none tracking-[1.17px]">
              Game Modeling Agent
            </p>
            <h1 className="max-w-3xl text-5xl font-bold uppercase leading-none tracking-[0.96px] md:text-6xl">
              GMA Frontend Controls
            </h1>
            <p className="mt-6 max-w-2xl text-base uppercase leading-7 text-[rgba(240,240,250,0.82)]">
              Stage 9.6 sends the modeling request and switches to a result page when the backend returns a structured
              response.
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
        </section>
      )}
    </main>
  );
}
