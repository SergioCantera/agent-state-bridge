import { useState } from "react";

export interface AgentChatMessage {
  role: "user" | "agent";
  content: string;
  timestamp?: number;
}

export interface AgentChatOptions<State = any> {
  endpoint?: string;
  initialMessages?: AgentChatMessage[];
  getState: () => State;
}

export function useAgentChat<State = any>({
  endpoint = "/chat",
  initialMessages = [],
  getState,
}: AgentChatOptions<State>) {
  const [messages, setMessages] = useState<AgentChatMessage[]>(initialMessages);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (userMessage: string) => {
    setLoading(true);
    setError(null);
    const newMsg: AgentChatMessage = { role: "user", content: userMessage, timestamp: Date.now() };
    setMessages((prev) => [...prev, newMsg]);
    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMessage,
          state: getState(),
        }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "agent", content: data.response, timestamp: Date.now() },
      ]);
    } catch (e: any) {
      setError(e.message || "Error sending message");
    } finally {
      setLoading(false);
    }
  };

  return { messages, sendMessage, loading, error };
}
