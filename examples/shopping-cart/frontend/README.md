# Shopping Cart Example - Frontend

React + Vite frontend using `agent-state-bridge` for AI-powered shopping assistance.

## Setup

```bash
npm install
```

## Install Dependencies

```bash
npm install agent-state-bridge react react-dom zustand react-markdown
npm install -D vite @vitejs/plugin-react tailwindcss
```

## Run Development Server

```bash
npm run dev
```

## Key Files

- `useAgentChat.js` - Custom hook using agent-state-bridge
- `AgentChat.jsx` - Chat UI component
- `cart.store.js` - Zustand store for cart management
- `products.json` - Products catalog (you need to create this)

## Example products.json

```json
[
  {
    "name": "Waffle with Berries",
    "category": "Waffle",
    "price": 6.5,
    "image": "/images/waffle.jpg"
  },
  {
    "name": "Vanilla Bean Crème Brûlée",
    "category": "Crème Brûlée",
    "price": 7.0,
    "image": "/images/creme-brulee.jpg"
  }
]
```

## Usage

```jsx
import { AgentChat } from "./AgentChat";

function App() {
  return (
    <div>
      <h1>My Shop</h1>
      <AgentChat />
    </div>
  );
}
```

## How It Works

1. User interacts with chat
2. `useAgentChat` hook sends message with current context:
   - Products catalog
   - Current cart state
   - Optional recent actions
3. Backend agent processes request and returns response
4. Agent can optionally return actions (add/remove/update cart)
5. Frontend executes actions via `onActionsReceived` callback
