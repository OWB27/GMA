type ResultPageHeaderProps = {
  gameName: string;
  jobId: string | null;
  status: string;
};

export function ResultPageHeader({ gameName, jobId, status }: ResultPageHeaderProps) {
  return (
    <header className="grid gap-6 md:grid-cols-[1fr_auto] md:items-end">
      <div>
        <p className="mb-3 text-[0.81rem] font-bold uppercase leading-none tracking-[1.17px]">
          Modeling Result
        </p>
        <h1 className="max-w-3xl text-5xl font-bold uppercase leading-none tracking-[0.96px] md:text-6xl">
          {gameName}
        </h1>
      </div>
      <div className="grid gap-3 border-t border-[rgba(240,240,250,0.24)] pt-5 text-sm uppercase leading-6 text-[rgba(240,240,250,0.78)] md:min-w-80">
        <div>
          <dt className="font-bold text-[#f0f0fa]">Status</dt>
          <dd className="m-0 break-words">{status}</dd>
        </div>
        <div>
          <dt className="font-bold text-[#f0f0fa]">Job ID</dt>
          <dd className="m-0 break-words">{jobId ?? "-"}</dd>
        </div>
      </div>
    </header>
  );
}
