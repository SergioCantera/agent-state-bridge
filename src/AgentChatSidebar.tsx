import React, { useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import type { AgentChatMessage } from "./useAgentChat";

export interface AgentChatSidebarProps {
  messages: AgentChatMessage[];
  onSend: (msg: string) => void;
  loading?: boolean;
  error?: string | null;
  open: boolean;
  onClose: () => void;
  title?: string;
  placeholder?: string;
  sendLabel?: string;
  className?: string;
  style?: React.CSSProperties;
}

export const AgentChatSidebar: React.FC<AgentChatSidebarProps> = ({
  messages,
  onSend,
  loading = false,
  error,
  open,
  onClose,
  title = "AI Assistant",
  placeholder = "Type your message...",
  sendLabel = "Send",
  className = "",
  style = {},
}) => {
  const [input, setInput] = React.useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, open]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      onSend(input);
      setInput("");
    }
  };

  if (!open) return null;

  return (
    <aside
      className={`fixed right-0 top-0 h-full w-80 bg-white shadow-lg z-50 flex flex-col ${className}`}
      style={style}
    >
      <header className="flex items-center justify-between p-4 border-b">
        <span className="font-bold text-lg">{title}</span>
        <button onClick={onClose} aria-label="Close chat" className="text-gray-500 hover:text-black">×</button>
      </header>
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 space-y-2 bg-gray-50"
        style={{ minHeight: 0 }}
      >
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`rounded px-3 py-2 max-w-[90%] whitespace-pre-wrap ${
              msg.role === "user"
                ? "bg-blue-100 self-end ml-auto"
                : "bg-gray-200 self-start mr-auto"
            }`}
          >
            <ReactMarkdown>{msg.content}</ReactMarkdown>
          </div>
        ))}
        {loading && (
          <div className="text-gray-400 italic">Thinking...</div>
        )}
        {error && (
          <div className="text-red-500 text-sm">{error}</div>
        )}
      </div>
      <form onSubmit={handleSend} className="p-4 border-t flex gap-2">
        <input
          className="flex-1 border rounded px-3 py-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={placeholder}
          disabled={loading}
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
          disabled={loading || !input.trim()}
        >
          {sendLabel}
        </button>
      </form>
    </aside>
  );
};
