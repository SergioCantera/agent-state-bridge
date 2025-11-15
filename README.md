# agent-state-bridge

**Full-stack bridge for sharing app state between frontend and AI agents.** Includes React hooks/components (npm) and Python backend utilities (PyPI) for FastAPI, Flask, and Django.

> 🚀 Build AI-powered apps with seamless state synchronization between your frontend and backend agents.

---

## 📦 Packages

This monorepo contains two complementary packages:

| Package | Platform | Description |
|---------|----------|-------------|
| **agent-state-bridge** | npm | React hooks and UI components for frontend |
| **agent-state-bridge** | PyPI | Python utilities for FastAPI, Flask, Django |

---

## 🎯 Frontend (React/TypeScript)

### Installation

```bash
npm install agent-state-bridge
```

### Quick Start

#### 1. Hook for state management

```tsx
import { useAgentChat } from "agent-state-bridge";

const { messages, sendMessage, loading, error } = useAgentChat({
  endpoint: "http://localhost:8000/chat",
  getState: () => myAppState, // Any state manager (Zustand, Redux, useState, etc.)
});
```

#### 2. Ready-to-use chat component

```tsx
import { AgentChatSidebar } from "agent-state-bridge";

<AgentChatSidebar
  messages={messages}
  onSend={sendMessage}
  loading={loading}
  error={error}
  open={open}
  onClose={() => setOpen(false)}
/>
```

### Features

✅ **State-agnostic**: Works with Zustand, Redux, useState, useContext, etc.  
✅ **UI included**: Pre-built chat component with markdown support  
✅ **Customizable**: Use hooks only or customize the UI  
✅ **TypeScript**: Fully typed  

📖 [Full Frontend Documentation →](./src/)

---

## 🐍 Backend (Python)

### Installation

```bash
# For FastAPI (recommended)
pip install agent-state-bridge[fastapi]

# For Flask
pip install agent-state-bridge[flask]

# For Django
pip install agent-state-bridge[django]
```

### Quick Start

#### FastAPI

```python
from fastapi import FastAPI
from agent_state_bridge.fastapi import create_agent_router

async def my_agent(message: str, state: dict) -> str:
    """Your agent logic here"""
    cart_items = state.get("cart", {}).get("items", [])
    return f"You have {len(cart_items)} items. You said: {message}"

app = FastAPI()
router = create_agent_router(my_agent, tags=["agent"])
app.include_router(router)
```

#### Flask

```python
from flask import Flask
from agent_state_bridge.flask import create_agent_blueprint

def my_agent(message: str, state: dict) -> str:
    return f"Processed: {message}"

app = Flask(__name__)
bp = create_agent_blueprint(my_agent)
app.register_blueprint(bp)
```

#### Django REST Framework

```python
from agent_state_bridge.django import agent_api_view

@agent_api_view
def my_agent(message: str, state: dict) -> str:
    return f"Processed: {message}"
```

### Agent Framework Support

✅ **LangChain**: Full async support  
✅ **Microsoft Agent Framework**: Azure AI integration  
✅ **CrewAI**: Multi-agent orchestration  
✅ **Custom agents**: Bring your own logic  

📖 [Full Backend Documentation →](./python/)  
📁 [Examples with LangChain, Agent Framework, etc. →](./python/examples/)

---

## 🚀 Complete Example

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

---

## 🚀 Complete Example

### Frontend (React)

```tsx
import React, { useState } from "react";
import { useAgentChat, AgentChatSidebar } from "agent-state-bridge";
import { useStore } from "./store"; // Zustand, Redux, or any state manager

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

### Backend (Python + FastAPI + LangChain)

```python
from fastapi import FastAPI
from agent_state_bridge.fastapi import create_agent_router
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

llm = ChatOpenAI(model="gpt-4o-mini")

async def langchain_agent(message: str, state: dict) -> str:
    cart_items = state.get("cart", {}).get("items", [])
    context = f"User has {len(cart_items)} items in cart."
    
    messages = [
        SystemMessage(content=f"You are a shopping assistant. {context}"),
        HumanMessage(content=message)
    ]
    
    response = await llm.ainvoke(messages)
    return response.content

app = FastAPI()
router = create_agent_router(langchain_agent, tags=["agent"])
app.include_router(router)
```

---

## 📚 API Reference

### Frontend (npm)

#### `useAgentChat(options)`

**Options:**
- `endpoint`: string (default: "/chat") - Backend endpoint URL
- `getState`: () => any (required) - Function returning current app state
- `initialMessages`: Message[] (optional) - Initial chat messages

**Returns:**
- `messages`: Message[] - Chat message history
- `sendMessage`: (msg: string) => Promise<void> - Send message to agent
- `loading`: boolean - Request in progress
- `error`: string | null - Error message if any

#### `<AgentChatSidebar>`

**Props:**
- `messages`, `onSend`, `loading`, `error`, `open`, `onClose` (required)
- `title`, `placeholder`, `sendLabel`, `className`, `style` (optional)

### Backend (PyPI)

#### FastAPI
- `create_agent_router(handler, prefix="", tags=[])` - Create router with `/chat` endpoint
- `AgentBridge` - Class-based approach with decorators

#### Flask
- `create_agent_blueprint(handler, name="agent", url_prefix="")` - Create blueprint
- `@agent_route` - Decorator for route handlers

#### Django
- `@agent_api_view` - Decorator for function-based views
- `AgentAPIView` - Base class for class-based views

---

## 🏗️ Architecture

```mermaid
graph LR
    A[React App] -->|HTTP POST| B[Backend API]
    A -->|state + message| B
    B -->|response| A
    B --> C[Agent Logic]
    C --> D[LangChain/Agent Framework/Custom]
```

**Key principles:**
- Frontend is the source of truth for state
- Backend is stateless (no session storage)
- State is sent with every request
- Works with any AI framework

📖 [Architecture Documentation →](./ARQUITECTURA_ESTADO.md)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details

---

## 🔗 Links

- **npm package**: [npmjs.com/package/agent-state-bridge](https://www.npmjs.com/package/agent-state-bridge)
- **PyPI package**: [pypi.org/project/agent-state-bridge](https://pypi.org/project/agent-state-bridge)
- **GitHub**: [github.com/SergioCantera/agent-state-bridge](https://github.com/SergioCantera/agent-state-bridge)
- **Issues**: [github.com/SergioCantera/agent-state-bridge/issues](https://github.com/SergioCantera/agent-state-bridge/issues)

---

**Made with ❤️ for the AI development community**
