# ToDo App - Frontend

Simple React + Vite frontend using native Context API and vanilla CSS.

## Key Features

- ✅ Native React state management (no external libraries)
- ✅ Vanilla CSS (no Tailwind or CSS-in-JS)
- ✅ Simple, clean component structure
- ✅ AI assistant integration with agent-state-bridge

## Setup

```bash
npm install
```

## Install Dependencies

```bash
npm install agent-state-bridge react react-dom
npm install -D vite @vitejs/plugin-react
```

## Run Development Server

```bash
npm run dev
```

## File Structure

```
frontend/
├── App.jsx              # Main app component
├── TodoContext.js       # Native Context API provider
├── TodoList.jsx         # Todo list with simple components
├── AgentChat.jsx        # Chat UI component
├── useAgentChat.js      # Hook using agent-state-bridge
└── styles.css           # Vanilla CSS styling
```

## Key Concepts

### 1. Native React Context

```javascript
// No Zustand, Redux, or external state libraries
import { createContext, useContext, useState } from 'react';

const TodoContext = createContext();

export const TodoProvider = ({ children }) => {
  const [todos, setTodos] = useState(INITIAL_TODOS);
  // ... state management logic
  return <TodoContext.Provider value={...}>{children}</TodoContext.Provider>;
};
```

### 2. Vanilla CSS

```css
/* Simple, readable CSS without frameworks */
.todo-item {
  display: flex;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}
```

### 3. Simple Components

```javascript
// Clean, minimal components
const Checkbox = ({ checked, onChange }) => (
  <input type="checkbox" checked={checked} onChange={onChange} />
);
```

## Usage

```jsx
import App from "./App";

// App already wrapped with TodoProvider
<App />;
```

## Learning Points

- How to use React Context API for global state
- Vanilla CSS organization and styling
- Simple component patterns
- Integration with AI assistant using agent-state-bridge
