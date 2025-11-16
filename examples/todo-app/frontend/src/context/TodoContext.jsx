import React, { createContext, useContext, useState } from 'react';

// Initial test data
const INITIAL_TODOS = [
  { id: 1, text: 'Complete project documentation', done: true },
  { id: 2, text: 'Review pull requests', done: true },
  { id: 3, text: 'Fix bug in authentication module', done: false },
  { id: 4, text: 'Prepare presentation for Monday', done: false },
  { id: 5, text: 'Update dependencies to latest versions', done: false },
  { id: 6, text: 'Write unit tests for new features', done: false },
  { id: 7, text: 'Schedule team meeting', done: true },
];

// Create context
const TodoContext = createContext();

/**
 * TodoProvider - Native React Context provider for todo state management
 * 
 * Uses only React built-in hooks (useState, useContext)
 * No external state management libraries (Zustand, Redux, etc.)
 */
export const TodoProvider = ({ children }) => {
  const [todos, setTodos] = useState(INITIAL_TODOS);

  // Add new todo
  const addTodo = (text) => {
    if (!text.trim()) return;
    
    const newTodo = {
      id: Date.now(),
      text: text.trim(),
      done: false
    };
    
    setTodos(prevTodos => [...prevTodos, newTodo]);
  };

  // Toggle todo done status
  const toggleTodo = (id) => {
    setTodos(prevTodos =>
      prevTodos.map(todo =>
        todo.id === id ? { ...todo, done: !todo.done } : todo
      )
    );
  };

  // Delete todo
  const deleteTodo = (id) => {
    setTodos(prevTodos => prevTodos.filter(todo => todo.id !== id));
  };

  // Clear all completed todos
  const clearCompleted = () => {
    setTodos(prevTodos => prevTodos.filter(todo => !todo.done));
  };

  // Get statistics
  const getStats = () => ({
    total: todos.length,
    completed: todos.filter(t => t.done).length,
    pending: todos.filter(t => !t.done).length
  });

  const value = {
    todos,
    addTodo,
    toggleTodo,
    deleteTodo,
    clearCompleted,
    getStats
  };

  return (
    <TodoContext.Provider value={value}>
      {children}
    </TodoContext.Provider>
  );
};

/**
 * Custom hook to use todo context
 */
export const useTodos = () => {
  const context = useContext(TodoContext);
  if (!context) {
    throw new Error('useTodos must be used within TodoProvider');
  }
  return context;
};
