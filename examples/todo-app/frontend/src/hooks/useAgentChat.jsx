import { useAgentChat } from 'agent-state-bridge';
import { useTodos } from '../context/TodoContext.jsx';

/**
 * Custom hook using agent-state-bridge with {messages, actions, context} model
 * 
 * Demonstrates integration with native React Context API
 */
export const useTodoAgentChat = () => {
  const { todos, addTodo, toggleTodo, deleteTodo, getStats } = useTodos();

  const { messages, sendMessage, loading, error } = useAgentChat({
    endpoint: 'http://localhost:8000/chat',
    
    // Context: Current todo state
    getContext: () => {
      const stats = getStats();
      return {
        todos: todos.map(t => ({
          id: t.id,
          text: t.text,
          done: t.done
        })),
        summary: {
          total: stats.total,
          completed: stats.completed,
          pending: stats.pending,
          completionRate: stats.total > 0 
            ? Math.round((stats.completed / stats.total) * 100) 
            : 0
        }
      };
    },
    
    // Actions: Recent user actions (optional)
    getActions: () => {
      return [];
    },
    
    // Handle actions from agent
    onActionsReceived: (actions) => {
      actions.forEach(action => {
        switch (action.type) {
          case 'post':
            // Add new todo
            if (action.payload?.text) {
              addTodo(action.payload.text);
            }
            break;
            
          case 'put':
            // Toggle todo status
            if (action.payload?.id) {
              toggleTodo(action.payload.id);
            }
            break;
            
          case 'delete':
            // Delete todo
            if (action.payload?.id) {
              deleteTodo(action.payload.id);
            }
            break;
        }
      });
    },
    
    initialMessages: []
  });

  return {
    messages,
    sendMessage,
    isLoading: loading,
    error
  };
};
