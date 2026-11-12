const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export type SupportCase = {
  id: string;
  customer_id: string;
  channel: string;
  status: string;
  intent: string;
  sentiment: number;
  priority: string;
  summary: string;
  recommended_resolution: string;
  payload: Record<string, unknown>;
};

export type Ticket = {
  id: string;
  case_id: string;
  status: string;
  owner: string | null;
  subject: string;
  priority: string;
  handover_required: boolean;
};

export type AnalyticsSummary = {
  total_cases: number;
  escalated_cases: number;
  open_tickets: number;
  average_sentiment: number;
  escalation_rate: number;
};

export async function createCase(payload: {
  customer_id: string;
  channel: string;
  message: string;
  attachments: Array<{ filename: string; content_type: string; extracted_text?: string }>;
}): Promise<SupportCase> {
  const response = await fetch(`${API_BASE_URL}/cases`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`Case creation failed with ${response.status}`);
  }
  return response.json();
}

export async function listCases(): Promise<SupportCase[]> {
  const response = await fetch(`${API_BASE_URL}/cases`);
  return response.json();
}

export async function listTickets(): Promise<Ticket[]> {
  const response = await fetch(`${API_BASE_URL}/tickets`);
  return response.json();
}

export async function getAnalytics(): Promise<AnalyticsSummary> {
  const response = await fetch(`${API_BASE_URL}/analytics/summary`);
  return response.json();
}
