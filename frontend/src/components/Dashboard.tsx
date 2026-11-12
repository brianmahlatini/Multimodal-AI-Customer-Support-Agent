import { Activity, MessageSquareWarning, TicketCheck, TrendingUp } from "lucide-react";
import { AnalyticsSummary } from "../lib/api";

export function Dashboard({ summary }: { summary: AnalyticsSummary | null }) {
  const cards = [
    { label: "Total cases", value: summary?.total_cases ?? 0, icon: Activity },
    { label: "Escalated", value: summary?.escalated_cases ?? 0, icon: MessageSquareWarning },
    { label: "Open tickets", value: summary?.open_tickets ?? 0, icon: TicketCheck },
    { label: "Escalation rate", value: `${Math.round((summary?.escalation_rate ?? 0) * 100)}%`, icon: TrendingUp },
  ];

  return (
    <section className="metrics-grid">
      {cards.map((card) => {
        const Icon = card.icon;
        return (
          <article className="metric" key={card.label}>
            <Icon size={20} />
            <span>{card.label}</span>
            <strong>{card.value}</strong>
          </article>
        );
      })}
    </section>
  );
}
