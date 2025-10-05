type Props = {
  title: string;
  dataset: string;
};

export function PlaceholderPage({ title, dataset }: Props) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>{title}</h2>
        <span>{dataset}</span>
      </div>
      <p className="muted">No published rows match the current filters.</p>
    </section>
  );
}
