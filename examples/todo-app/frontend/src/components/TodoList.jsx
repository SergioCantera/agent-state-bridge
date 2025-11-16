import React, { useState } from 'react';
import { useTodos } from '../context/TodoContext.jsx';

/**
 * Simple Checkbox component
 */
const Checkbox = ({ checked, onChange, id }) => (
  <input
    type="checkbox"
    id={id}
    checked={checked}
    onChange={onChange}
    className="checkbox"
  />
);

/**
 * Simple Label component
 */
const Label = ({ htmlFor, children, done }) => (
  <label
    htmlFor={htmlFor}
    className={`todo-label ${done ? 'done' : ''}`}
  >
    {children}
  </label>
);

/**
 * Simple TextInput component
 */
const TextInput = ({ value, onChange, onKeyPress, placeholder }) => (
  <input
    type="text"
    value={value}
    onChange={onChange}
    onKeyPress={onKeyPress}
    placeholder={placeholder}
    className="text-input"
  />
);

/**
 * TodoList component - Displays and manages todos
 */
export const TodoList = () => {
  const { todos, addTodo, toggleTodo, deleteTodo, clearCompleted, getStats } = useTodos();
  const [inputValue, setInputValue] = useState('');
  const stats = getStats();

  const handleAddTodo = () => {
    if (inputValue.trim()) {
      addTodo(inputValue);
      setInputValue('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleAddTodo();
    }
  };

  return (
    <div className="todo-container">
      <div className="todo-header">
        <h1>My Tasks</h1>
        <div className="stats">
          <span className="stat">Total: {stats.total}</span>
          <span className="stat">Pending: {stats.pending}</span>
          <span className="stat completed">Done: {stats.completed}</span>
        </div>
      </div>

      {/* Add todo input */}
      <div className="add-todo">
        <TextInput
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="What needs to be done?"
        />
        <button onClick={handleAddTodo} className="btn-add">
          Add Task
        </button>
      </div>

      {/* Todo list */}
      <div className="todo-list">
        {todos.length === 0 ? (
          <div className="empty-state">
            <p>No tasks yet. Add one above!</p>
          </div>
        ) : (
          todos.map(todo => (
            <div key={todo.id} className="todo-item">
              <Checkbox
                id={`todo-${todo.id}`}
                checked={todo.done}
                onChange={() => toggleTodo(todo.id)}
              />
              <Label htmlFor={`todo-${todo.id}`} done={todo.done}>
                {todo.text}
              </Label>
              <button
                onClick={() => deleteTodo(todo.id)}
                className="btn-delete"
                aria-label="Delete task"
              >
                ✕
              </button>
            </div>
          ))
        )}
      </div>

      {/* Actions */}
      {stats.completed > 0 && (
        <div className="todo-actions">
          <button onClick={clearCompleted} className="btn-clear">
            Clear Completed ({stats.completed})
          </button>
        </div>
      )}
    </div>
  );
};
