import { type FormEvent, useState } from "react";

import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";

type ModelingJobForm = {
  gameName: string;
  steamUrl: string;
};

export default function App() {
  const [form, setForm] = useState<ModelingJobForm>({
    gameName: "",
    steamUrl: "",
  });
  const [submittedJob, setSubmittedJob] = useState<ModelingJobForm | null>(null);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmittedJob(form);
  }

  function handleReset() {
    setForm({
      gameName: "",
      steamUrl: "",
    });
    setSubmittedJob(null);
  }

  return (
    <main className="min-h-screen bg-black px-6 py-10 text-[#f0f0fa] font-din">
      <section className="mx-auto grid min-h-[calc(100vh-80px)] max-w-6xl items-end gap-12 md:grid-cols-[1.1fr_0.9fr]">
        <div>
          <p className="mb-3 text-[0.81rem] font-bold uppercase leading-none tracking-[1.17px]">
            Game Modeling Agent
          </p>
          <h1 className="max-w-3xl text-5xl font-bold uppercase leading-none tracking-[0.96px] md:text-6xl">
            GMA Frontend Controls
          </h1>
          <p className="mt-6 max-w-2xl text-base uppercase leading-7 text-[rgba(240,240,250,0.82)]">
            Stage 9.3 turns the static controls into a controlled React form. API wiring comes later; for now we only
            prove that form state moves through React correctly.
          </p>
        </div>

        <form className="grid gap-8" onSubmit={handleSubmit}>
          <div className="grid gap-3">
            <Label htmlFor="game-name">Game Name</Label>
            <Input
              id="game-name"
              value={form.gameName}
              onChange={(event) => {
                setForm({
                  ...form,
                  gameName: event.target.value,
                });
              }}
              placeholder="e.g., Arc Raiders"
              required
            />
          </div>
          <div className="grid gap-3">
            <Label htmlFor="steam-url">Steam URL</Label>
            <Input
              id="steam-url"
              value={form.steamUrl}
              onChange={(event) => {
                setForm({
                  ...form,
                  steamUrl: event.target.value,
                });
              }}
              placeholder="https://store.steampowered.com/app/..."
              required
            />
          </div>
          <div className="flex flex-wrap gap-3">
            <Button type="submit">Run Modeling</Button>
            <Button type="button" variant="quiet" onClick={handleReset}>
              Reset
            </Button>
          </div>
          {submittedJob ? (
            <section className="border-t border-[rgba(240,240,250,0.24)] pt-5">
              <p className="mb-3 text-[0.63rem] font-bold uppercase leading-none tracking-[1px]">
                Submitted Job Preview
              </p>
              <dl className="grid gap-3 text-sm uppercase leading-6 text-[rgba(240,240,250,0.78)]">
                <div>
                  <dt className="font-bold text-[#f0f0fa]">Game Name</dt>
                  <dd className="m-0 break-words">{submittedJob.gameName}</dd>
                </div>
                <div>
                  <dt className="font-bold text-[#f0f0fa]">Steam URL</dt>
                  <dd className="m-0 break-words">{submittedJob.steamUrl}</dd>
                </div>
              </dl>
            </section>
          ) : null}
        </form>
      </section>
    </main>
  );
}
