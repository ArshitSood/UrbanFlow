import { useMutation } from "@tanstack/react-query";
import { Send } from "lucide-react";
import { FormEvent, useState } from "react";
import { askAgent } from "../../services/api";

export function AgentDrawer() {
  const [question, setQuestion] = useState("What is the latest pipeline status?");
  const mutation = useMutation({
    mutationFn: () => askAgent(question, { date_range: ["2026-01-01", "2026-01-31"], service_type: "yellow" }),
  });

  function submit(event: FormEvent) {
    event.preventDefault();
    mutation.mutate();
  }

  return (
    <aside className="agent-drawer" aria-label="Contextual agent">
      <h2>Agent</h2>
      <div className="chips">
        <span>yellow</span>
        <span>Jan 2026</span>
        <span>read-only</span>
      </div>
      <form onSubmit={submit} className="agent-form">
        <textarea value={question} onChange={(event) => setQuestion(event.target.value)} aria-label="Agent question" />
        <button type="submit" aria-label="Ask agent">
          <Send size={16} aria-hidden />
        </button>
      </form>
      {mutation.data && (
        <div className="agent-answer">
          <strong>{mutation.data.answer}</strong>
          <pre>{JSON.stringify(mutation.data.provenance, null, 2)}</pre>
        </div>
      )}
      {mutation.error && <p className="error">Agent request failed.</p>}
    </aside>
  );
}

