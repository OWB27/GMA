export type GRSExportRecord = {
  game_code: string;
  tag_code: string;
  weight: number;
};

export type GRSExportPayload = GRSExportRecord[];
