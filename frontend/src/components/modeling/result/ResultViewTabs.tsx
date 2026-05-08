import { Button } from "../../ui/button";

export type ResultView = "steam-evidence" | "ai-tags" | "human-review";

type ResultViewTabsProps = {
  activeView: ResultView;
  onViewChange: (view: ResultView) => void;
};

export function ResultViewTabs({ activeView, onViewChange }: ResultViewTabsProps) {
  return (
    <div className="flex flex-wrap gap-3 border-b border-[rgba(240,240,250,0.24)] pb-5">
      <Button
        type="button"
        variant={activeView === "steam-evidence" ? "ghost" : "quiet"}
        onClick={() => onViewChange("steam-evidence")}
      >
        Steam Evidence
      </Button>
      <Button
        type="button"
        variant={activeView === "ai-tags" ? "ghost" : "quiet"}
        onClick={() => onViewChange("ai-tags")}
      >
        AI Tags
      </Button>
      <Button
        type="button"
        variant={activeView === "human-review" ? "ghost" : "quiet"}
        onClick={() => onViewChange("human-review")}
      >
        Human Review
      </Button>
    </div>
  );
}
