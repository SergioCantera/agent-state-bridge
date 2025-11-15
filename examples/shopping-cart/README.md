# Shopping Cart Example

Complete example of an AI-powered shopping cart using `agent-state-bridge` with the `{messages, actions, context}` model.

## Architecture

- **Frontend**: React + Vite + Zustand (state management)
- **Backend**: Python + FastAPI + LangChain
- **AI Model**: GitHub Models (gpt-4o-mini)

## Features

✅ Chat with AI assistant about products
✅ AI can recommend products based on conversation
✅ Full cart state shared with agent
✅ Bidirectional actions (agent can suggest cart operations)
✅ RAG-ready architecture (context prepared for vector search)

## Project Structure

```
shopping-cart/
├── frontend/           # React app
│   ├── useAgentChat.js    # Hook using agent-state-bridge
│   ├── AgentChat.jsx      # Chat UI component
│   └── cart.store.js      # Zustand store
├── backend/            # FastAPI app
│   ├── agent.py           # LangChain agent with {messages, actions, context}
│   └── requirements.txt
└── README.md
```

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt

# Set environment variables
export LLM_API_KEY="your-github-token"
export LLM_BASE_URL="https://models.inference.ai.azure.com"
export LLM_MODEL_ID="gpt-4o-mini"

# Run server
python agent.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Key Concepts

### 1. Separating Actions from Context

```javascript
// Frontend hook
const { messages, sendMessage } = useAgentChat({
  endpoint: 'http://localhost:8000/chat',
  
  // Context: App state + RAG data (could include vector search results)
  getContext: () => ({
    products: availableProducts,
    cart: currentCartState
  }),
  
  // Actions: Recent CRUD operations (optional, for tracking)
  getActions: () => recentActions,
  
  // Handle actions returned by agent
  onActionsReceived: (actions) => {
    actions.forEach(action => {
      if (action.type === 'post') addToCart(action.payload.productName);
      if (action.type === 'delete') removeFromCart(action.payload.productName);
    });
  }
});
```

### 2. Backend Agent Handler

```python
from agent_state_bridge.models import AgentResponse, Message, Action

async def shopping_agent(
    messages: list[Message],    # Conversation history
    actions: list[Action],       # Recent CRUD operations
    context: dict               # App state + RAG data
) -> AgentResponse:
    # Access full context
    cart = context.get('cart', {})
    products = context.get('products', [])
    
    # Build response using LangChain
    response_text = await build_response(messages, cart, products)
    
    # Optionally return actions for frontend to execute
    return AgentResponse(
        response=response_text,
        actions=[Action(type="post", payload={"productName": "Waffle"})],
        context=None  # Optional: return updated context
    )
```

### 3. Why This Model?

**Before (v0.1.0):**
```python
async def agent(message: str, state: dict) -> str:
    # Everything mixed together
    # Hard to separate concerns
    # Not RAG-ready
```

**After (v0.2.0):**
```python
async def agent(messages, actions, context) -> AgentResponse:
    # ✅ Message history separate
    # ✅ CRUD operations tracked
    # ✅ Context ready for RAG data
    # ✅ Can return actions for frontend
```

## Benefits

1. **Scalable**: Easy to add RAG, vector search, or multiple agents
2. **Clear separation**: Actions (mutations) vs Context (state)
3. **Bidirectional**: Agent can suggest actions, frontend executes them
4. **Type-safe**: Full TypeScript and Pydantic support
5. **Framework-agnostic**: Works with any state manager and AI framework

## Learn More

- [agent-state-bridge Documentation](../../README.md)
- [API Reference](../../README.md#-api-reference)
- [Architecture Guide](../../ARQUITECTURA_ESTADO.md)
