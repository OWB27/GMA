import { useEffect, useState } from "react";

import { GRS_TAG_CODES, type GrsTagCode } from "../../constants/grsTags";
import type { SelectedTagSuggestion } from "../../types/api";
import type { ReviewTagDraft } from "../../types/review";
import { Button } from "../ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";

type HumanReviewSectionProps = {
  selectedTags: SelectedTagSuggestion[];
};

function createDraftsFromSuggestions(selectedTags: SelectedTagSuggestion[]): ReviewTagDraft[] {
  return selectedTags.map((tag) => ({
    tagCode: normalizeTagCode(tag.tag_code),
    weight: tag.suggested_weight,
  }));
}

function normalizeTagCode(tagCode: string): GrsTagCode {
  return GRS_TAG_CODES.includes(tagCode as GrsTagCode) ? (tagCode as GrsTagCode) : GRS_TAG_CODES[0];
}

export function HumanReviewSection({ selectedTags }: HumanReviewSectionProps) {
  const [tagDrafts, setTagDrafts] = useState<ReviewTagDraft[]>(() =>
    createDraftsFromSuggestions(selectedTags),
  );

  useEffect(() => {
    setTagDrafts(createDraftsFromSuggestions(selectedTags));
  }, [selectedTags]);

  function updateTagDraft(index: number, patch: Partial<ReviewTagDraft>) {
    setTagDrafts((currentDrafts) =>
      currentDrafts.map((draft, currentIndex) =>
        currentIndex === index ? { ...draft, ...patch } : draft,
      ),
    );
  }

  function removeTagDraft(index: number) {
    setTagDrafts((currentDrafts) => currentDrafts.filter((_, currentIndex) => currentIndex !== index));
  }

  function addTagDraft() {
    setTagDrafts((currentDrafts) => [...currentDrafts, { tagCode: GRS_TAG_CODES[0], weight: 3 }]);
  }

  return (
    <section className="border-t border-[rgba(240,240,250,0.24)] pt-8">
      <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold uppercase tracking-[0.96px]">Human Review</h2>
          <p className="mt-3 max-w-2xl text-sm uppercase leading-6 text-[rgba(240,240,250,0.72)]">
            Edit the AI tag draft locally before this page connects to the review API.
          </p>
        </div>
        <Button type="button" variant="quiet" onClick={addTagDraft}>
          Add Tag
        </Button>
      </div>

      <div className="grid gap-5">
        {tagDrafts.map((draft, index) => (
          <article
            className="grid gap-4 border-b border-[rgba(240,240,250,0.18)] pb-5 md:grid-cols-[1fr_160px_auto] md:items-end"
            key={`${draft.tagCode}-${index}`}
          >
            <label className="grid gap-2">
              <span className="text-[0.68rem] font-bold uppercase tracking-[1.17px] text-[rgba(240,240,250,0.72)]">
                Tag Code
              </span>
              <Select
                value={draft.tagCode}
                onValueChange={(value) => updateTagDraft(index, { tagCode: value as GrsTagCode })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select tag" />
                </SelectTrigger>
                <SelectContent>
                  {GRS_TAG_CODES.map((tagCode) => (
                    <SelectItem key={tagCode} value={tagCode}>
                      {tagCode}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </label>

            <label className="grid gap-2">
              <span className="text-[0.68rem] font-bold uppercase tracking-[1.17px] text-[rgba(240,240,250,0.72)]">
                Weight
              </span>
              <Select
                value={String(draft.weight)}
                onValueChange={(value) => updateTagDraft(index, { weight: Number(value) })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select weight" />
                </SelectTrigger>
                <SelectContent>
                  {[1, 2, 3, 4, 5].map((weight) => (
                    <SelectItem key={weight} value={String(weight)}>
                      {weight}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </label>

            <Button type="button" variant="quiet" onClick={() => removeTagDraft(index)}>
              Remove
            </Button>
          </article>
        ))}
      </div>
    </section>
  );
}
