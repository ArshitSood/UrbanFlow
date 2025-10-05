import { useQuery } from "@tanstack/react-query";
import { fetchPipelines, fetchQualityRuns } from "../services/api";

type Props = {
  view: "quality" | "pipelines";
};

export function OperationsPage({ view }: Props) {
  const quality = useQuery({ queryKey: ["quality"], queryFn: fetchQualityRuns, enabled: view === "quality" });
  const pipelines = useQuery({ queryKey: ["pipelines"], queryFn: fetchPipelines, enabled: view === "pipelines" });
  const rows = view === "quality" ? quality.data : pipelines.data;
  const isLoading = view === "quality" ? quality.isLoading : pipelines.isLoading;

  if (isLoading) return <section className="panel">Loading {view}...</section>;

  return (
    <section className="panel table-panel">
      <div className="panel-heading">
        <h2>{view === "quality" ? "Data Quality Runs" : "Pipeline Runs"}</h2>
        <span>server-backed</span>
      </div>
      <table>
        <thead>
          <tr>
            {rows?.[0] &&
              Object.keys(rows[0]).map((key) => (
                <th key={key} scope="col">
                  {key}
                </th>
              ))}
          </tr>
        </thead>
        <tbody>
          {rows?.map((row, index) => (
            <tr key={index}>
              {Object.values(row).map((value, cellIndex) => (
                <td key={cellIndex}>{String(value)}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

