type ModelingRunNoticeProps = {
  errorMessage: string | null;
};

export function ModelingRunNotice({ errorMessage }: ModelingRunNoticeProps) {
  if (!errorMessage) {
    return null;
  }

  return (
    <p className="text-sm uppercase leading-6 text-[rgba(240,240,250,0.86)]">
      Request error: {errorMessage}
    </p>
  );
}
