type ResultBlockProps = {
  title: string;
  children: string;
};

export function ResultBlock({ title, children }: ResultBlockProps) {
  return (
    <section className="border-b border-[rgba(240,240,250,0.24)] py-5">
      <h3 className="mb-3 text-[0.63rem] font-bold uppercase leading-none tracking-[1px]">{title}</h3>
      <p className="m-0 whitespace-pre-wrap break-words text-sm uppercase leading-6 text-[rgba(240,240,250,0.82)]">
        {children}
      </p>
    </section>
  );
}
