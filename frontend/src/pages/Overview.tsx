import { useQuery } from "@tanstack/react-query";
import { AlertTriangle, CheckCircle2, Clock, Database } from "lucide-react";
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { fetchOverview } from "../services/api";

export function Overview() {
  const { data, isLoading, error } = useQuery({ queryKey: ["overview"], queryFn: fetchOverview });

  if (isLoading) return <section className="panel">Loading overview...</section>;
  if (error || !data) return <section className="panel error">Overview could not be loaded.</section>;

  return (
    <div className="page-grid">
      <section className="metric-card">
        <Database aria-hidden size={18} />
        <span>Trips Processed</span>
        <strong>{data.kpis.trips_processed.toLocaleString()}</strong>
      </section>
      <section className="metric-card">
        <CheckCircle2 aria-hidden size={18} />
        <span>Quality Gate</span>
        <strong>{data.kpis.quality_gate}</strong>
      </section>
      <section className="metric-card">
        <Clock aria-hidden size={18} />
        <span>Latest Source</span>
        <strong>{data.data_freshness.latest_source_month}</strong>
      </section>
      <section className="metric-card">
        <AlertTriangle aria-hidden size={18} />
        <span>Pipeline Health</span>
        <strong>{data.kpis.pipeline_health}</strong>
      </section>

      <section className="panel wide">
        <div className="panel-heading">
          <h2>Trip Volume</h2>
          <span>{data.source_dataset}</span>
        </div>
        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={data.trend}>
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="trip_count" stroke="#08776f" strokeWidth={2} dot />
          </LineChart>
        </ResponsiveContainer>
      </section>

      <section className="panel">
        <div className="panel-heading">
          <h2>Operational Status</h2>
          <span>{data.query_id}</span>
        </div>
        <dl className="definition-list">
          <dt>Freshness</dt>
          <dd>{data.data_freshness.warehouse_published_at}</dd>
          <dt>Filters</dt>
          <dd>{JSON.stringify(data.applied_filters)}</dd>
        </dl>
      </section>
    </div>
  );
}

