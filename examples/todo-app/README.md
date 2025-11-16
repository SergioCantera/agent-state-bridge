# ToDo App Example

Simple AI-powered ToDo list using `agent-state-bridge` with native React Context API and vanilla CSS.

## Architecture

- **Frontend**: React + Vite + Context API (no external state library)
- **Backend**: Python + FastAPI + LangChain
- **Styling**: Vanilla CSS (no Tailwind)
- **AI Model**: GitHub Models (gpt-4o-mini)

## Features

✅ Create, complete, and delete todos
✅ Chat with AI assistant about your tasks
✅ AI understands full todo context
✅ Native React state management (Context API)
✅ Simple vanilla CSS styling
✅ RAG-ready architecture

## Project Structure

```
todo-app/
├── frontend/           # React app
│   ├── TodoContext.js     # Context provider with native hooks
│   ├── useAgentChat.js    # Hook using agent-state-bridge
│   ├── App.jsx            # Main app component
│   ├── TodoList.jsx       # Todo list component
│   ├── AgentChat.jsx      # Chat UI component
│   └── styles.css         # Vanilla CSS
├── backend/            # FastAPI app
│   ├── agent.py           # LangChain agent
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

### 1. Native React Context for State Management

```javascript
// No Zustand, Redux, or external libraries
// Pure React with useState + useContext
const TodoContext = createContext();

export const TodoProvider = ({ children }) => {
  const [todos, setTodos] = useState(INITIAL_TODOS);

  const addTodo = (text) => {
    /* ... */
  };
  const toggleTodo = (id) => {
    /* ... */
  };
  const deleteTodo = (id) => {
    /* ... */
  };

  return (
    <TodoContext.Provider value={{ todos, addTodo, toggleTodo, deleteTodo }}>
      {children}
    </TodoContext.Provider>
  );
};
```

### 2. Vanilla CSS Styling

```css
/* Simple, clean CSS without Tailwind */
.todo-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #eee;
}
```

### 3. AI Agent Integration

```javascript
const { messages, sendMessage } = useAgentChat({
  getContext: () => ({
    todos: todos,
    summary: {
      total: todos.length,
      completed: todos.filter((t) => t.done).length,
      pending: todos.filter((t) => !t.done).length,
    },
  }),
});
```

## Benefits

1. **Simple**: No complex state libraries or CSS frameworks
2. **Native**: Uses only React built-in features
3. **Learning**: Great for understanding Context API
4. **AI-powered**: Assistant helps manage and organize tasks
5. **Scalable**: Easy to add RAG for task recommendations

## Learn More

- [agent-state-bridge Documentation](../../README.md)
- [React Context API](https://react.dev/reference/react/createContext)
- [Shopping Cart Example](../shopping-cart/) - More complex example
