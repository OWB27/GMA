import type { FormEvent } from "react";

import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";

export type ModelingJobForm = {
  gameName: string;
  steamUrl: string;
};

type CreateModelingJobFormProps = {
  form: ModelingJobForm;
  isRunning: boolean;
  onFormChange: (form: ModelingJobForm) => void;
  onReset: () => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
};

export function CreateModelingJobForm({
  form,
  isRunning,
  onFormChange,
  onReset,
  onSubmit,
}: CreateModelingJobFormProps) {
  return (
    <form className="grid gap-8" onSubmit={onSubmit}>
      <div className="grid gap-3">
        <Label htmlFor="game-name">Game Name</Label>
        <Input
          id="game-name"
          value={form.gameName}
          onChange={(event) => {
            onFormChange({
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
            onFormChange({
              ...form,
              steamUrl: event.target.value,
            });
          }}
          placeholder="https://store.steampowered.com/app/..."
          required
        />
      </div>
      <div className="flex flex-wrap gap-3">
        <Button type="submit" disabled={isRunning}>
          {isRunning ? "Running" : "Run Modeling"}
        </Button>
        <Button type="button" variant="quiet" onClick={onReset} disabled={isRunning}>
          Reset
        </Button>
      </div>
    </form>
  );
}
