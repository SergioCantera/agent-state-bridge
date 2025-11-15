# agent-state-bridge

Bridge para compartir el estado de tu app y chat con un agente Python (FastAPI) de forma sencilla y reutilizable.

## Instalación

```bash
npm install agent-state-bridge
```

## Uso rápido

### 1. Hook principal

```tsx
import { useAgentChat } from "agent-state-bridge";

const { messages, sendMessage, loading, error } = useAgentChat({
  endpoint: "http://localhost:8000/chat", // o tu endpoint
  getState: () => myAppState, // función que retorna el estado actual
});
```

### 2. Componente de chat listo para usar

```tsx
import { AgentChatSidebar } from "agent-state-bridge";

<AgentChatSidebar
  messages={messages}
  onSend={sendMessage}
  loading={loading}
  error={error}
  open={open}
  onClose={() => setOpen(false)}
/>;
```

### 3. Personalización

- Puedes usar solo el hook y crear tu propio componente de chat.
- El componente AgentChatSidebar acepta props para personalizar título, placeholder, estilos, etc.

## Ejemplo completo

```tsx
import React, { useState } from "react";
import { useAgentChat, AgentChatSidebar } from "agent-state-bridge";
import { useStore } from "./store"; // tu store Zustand

export function MyChat() {
  const [open, setOpen] = useState(false);
  const cart = useStore((s) => s.cart);
  const { messages, sendMessage, loading, error } = useAgentChat({
    endpoint: "http://localhost:8000/chat",
    getState: () => ({ cart }),
  });
  return (
    <>
      <button onClick={() => setOpen(true)}>Open Chat</button>
      <AgentChatSidebar
        messages={messages}
        onSend={sendMessage}
        loading={loading}
        error={error}
        open={open}
        onClose={() => setOpen(false)}
        title="Shopping Assistant"
      />
    </>
  );
}
```

## API

### useAgentChat(options)

- `endpoint`: string (opcional, default: "/chat")
- `getState`: función que retorna el estado actual (obligatorio)
- `initialMessages`: mensajes iniciales (opcional)

Devuelve: `{ messages, sendMessage, loading, error }`

### AgentChatSidebar props

- `messages`, `onSend`, `loading`, `error`, `open`, `onClose` (obligatorios)
- `title`, `placeholder`, `sendLabel`, `className`, `style` (opcionales)

## Extensión

- Puedes crear tu propio componente de chat usando solo el hook.
- El payload enviado al backend incluye `{ message, state }`.

---

¿Dudas o sugerencias? ¡Abre un issue o PR!
