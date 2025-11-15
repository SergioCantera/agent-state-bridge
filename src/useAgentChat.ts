import { useState } from "react";

export interface AgentChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp?: number;
}

export interface AgentAction {
  type: string;
  payload?: Record<string, any>;
}

export interface AgentChatOptions<Context = any> {
  endpoint?: string;
  initialMessages?: AgentChatMessage[];
  getContext: () => Context;
  getActions?: () => AgentAction[];
  onActionsReceived?: (actions: AgentAction[]) => void;
  onContextUpdated?: (context: Context) => void;
}

export function useAgentChat<Context = any>({
  endpoint = "/chat",
  initialMessages = [],
  getContext,
  getActions = () => [],
  onActionsReceived,
  onContextUpdated,
}: AgentChatOptions<Context>) {
  const [messages, setMessages] = useState<AgentChatMessage[]>(initialMessages);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (userMessage: string) => {
    setLoading(true);
    setError(null);
    
    const newMsg: AgentChatMessage = { 
      role: "user", 
      content: userMessage, 
      timestamp: Date.now() 
    };
    
    const updatedMessages = [...messages, newMsg];
    setMessages(updatedMessages);
    
    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: updatedMessages.map(m => ({ role: m.role, content: m.content })),
          actions: getActions(),
          context: getContext(),
        }),
      });
      
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }
      
      const data = await res.json();
      
      // Add assistant response
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response, timestamp: Date.now() },
      ]);
      
      // Handle returned actions
      if (data.actions && onActionsReceived) {
        onActionsReceived(data.actions);
      }
      
      // Handle updated context
      if (data.context && onContextUpdated) {
        onContextUpdated(data.context);
      }
      
    } catch (e: any) {
      setError(e.message || "Error sending message");
    } finally {
      setLoading(false);
    }
  };

  return { messages, sendMessage, loading, error };
}
