import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";

export default function App() {
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
            Stage 9.2 adds Tailwind CSS and shadcn-style base components. This form is still static; API wiring comes
            later.
          </p>
        </div>

        <form className="grid gap-8">
          <div className="grid gap-3">
            <Label htmlFor="game-name">Game Name</Label>
            <Input id="game-name" placeholder="e.g., Arc Raiders" />
          </div>
          <div className="grid gap-3">
            <Label htmlFor="steam-url">Steam URL</Label>
            <Input id="steam-url" placeholder="https://store.steampowered.com/app/..." />
          </div>
          <div className="flex flex-wrap gap-3">
            <Button type="button">Run Modeling</Button>
            <Button type="button" variant="quiet">
              Reset
            </Button>
          </div>
        </form>
      </section>
    </main>
  );
}
