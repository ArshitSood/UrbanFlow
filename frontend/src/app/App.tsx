import { Activity, Database, GitBranch, Plane, Route, Settings, ShieldCheck, SquareStack, WalletCards } from "lucide-react";
import { NavLink, Route as RouterRoute, Routes } from "react-router-dom";
import { AgentDrawer } from "../components/agents/AgentDrawer";
import { Overview } from "../pages/Overview";
import { OperationsPage } from "../pages/OperationsPage";
import { PlaceholderPage } from "../pages/PlaceholderPage";

const navItems = [
  { to: "/", label: "Overview", icon: Activity },
  { to: "/mobility", label: "Mobility", icon: SquareStack },
  { to: "/routes", label: "Routes", icon: Route },
  { to: "/airports", label: "Airports", icon: Plane },
  { to: "/revenue", label: "Revenue", icon: WalletCards },
  { to: "/quality", label: "Quality", icon: ShieldCheck },
  { to: "/pipelines", label: "Pipelines", icon: Database },
  { to: "/lineage", label: "Lineage", icon: GitBranch },
  { to: "/settings", label: "Settings", icon: Settings },
];

export function App() {
  return (
    <div className="shell">
      <aside className="sidebar" aria-label="Primary navigation">
        <div className="brand">UrbanFlow</div>
        <nav>
          {navItems.map((item) => (
            <NavLink key={item.to} to={item.to} className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}>
              <item.icon size={18} aria-hidden />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Production data product</p>
            <h1>Urban mobility control plane</h1>
          </div>
          <div className="filters" aria-label="Global filters">
            <select aria-label="Service type" defaultValue="yellow">
              <option value="yellow">Yellow</option>
              <option value="green">Green</option>
              <option value="fhvhv">FHVHV</option>
            </select>
            <input aria-label="Start date" type="date" defaultValue="2026-01-01" />
            <input aria-label="End date" type="date" defaultValue="2026-01-31" />
            <span className="env">dev</span>
          </div>
        </header>
        <Routes>
          <RouterRoute path="/" element={<Overview />} />
          <RouterRoute path="/quality" element={<OperationsPage view="quality" />} />
          <RouterRoute path="/pipelines" element={<OperationsPage view="pipelines" />} />
          <RouterRoute path="/mobility" element={<PlaceholderPage title="Mobility Explorer" dataset="gold.hourly_zone_demand" />} />
          <RouterRoute path="/routes" element={<PlaceholderPage title="Route Performance" dataset="gold.route_performance" />} />
          <RouterRoute path="/airports" element={<PlaceholderPage title="Airport Analytics" dataset="gold.airport_metrics" />} />
          <RouterRoute path="/revenue" element={<PlaceholderPage title="Revenue" dataset="gold.revenue_metrics" />} />
          <RouterRoute path="/lineage" element={<PlaceholderPage title="Lineage" dataset="metadata.lineage" />} />
          <RouterRoute path="/settings" element={<PlaceholderPage title="System Settings" dataset="metadata.system" />} />
        </Routes>
      </main>
      <AgentDrawer />
    </div>
  );
}

