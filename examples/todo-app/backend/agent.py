"""
Todo Assistant Agent using agent-state-bridge with {messages, actions, context} model

This example demonstrates:
- AI assistant for task management
- Using native React Context API for state
- Simple vanilla CSS styling
- Integration with agent-state-bridge
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from agent_state_bridge.fastapi import create_agent_router
from agent_state_bridge.models import AgentResponse, Message, Action

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Todo Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LangChain model
model = ChatOpenAI(
    model=os.getenv("LLM_MODEL_ID", "gpt-4o-mini"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    temperature=0.7,
)


async def todo_agent(
    messages: List[Message], 
    actions: List[Action], 
    context: Dict[str, Any]
) -> AgentResponse:
    """
    Todo assistant agent handler.
    
    Args:
        messages: Conversation history with user
        actions: Recent CRUD operations on todos (optional)
        context: Current application state including:
            - todos: List of all todos with id, text, done status
            - summary: Statistics (total, completed, pending, completionRate)
    
    Returns:
        AgentResponse containing:
            - response: Agent's text response
            - actions: Optional list of actions for frontend to execute
            - context: Optional updated context
    """
    
    # Extract context data
    todos = context.get('todos', [])
    summary = context.get('summary', {})
    
    # Build todo lists
    pending_todos = [t for t in todos if not t.get('done', False)]
    completed_todos = [t for t in todos if t.get('done', False)]
    
    # Format todo lists for prompt
    if pending_todos:
        pending_list = "\n".join([f"  {i+1}. ID={t['id']}: {t['text']}" for i, t in enumerate(pending_todos)])
    else:
        pending_list = "  (none)"
    
    if completed_todos:
        completed_list = "\n".join([f"  ✓ ID={t['id']}: {t['text']}" for t in completed_todos])
    else:
        completed_list = "  (none)"
    
    # Build recent actions context
    actions_context = ""
    if actions:
        actions_context = "\n\nRECENT USER ACTIONS:\n" + "\n".join([
            f"- {action.type}: {action.payload}" for action in actions
        ])
    
    # Build system prompt
    system_content = f"""You are a helpful todo list assistant. Help users manage their tasks effectively.

CURRENT TASK STATUS:
Total tasks: {summary.get('total', 0)}
Completed: {summary.get('completed', 0)}
Pending: {summary.get('pending', 0)}
Completion rate: {summary.get('completionRate', 0)}%

PENDING TASKS:
{pending_list}

COMPLETED TASKS:
{completed_list}
{actions_context}

IMPORTANT: When users ask you to create, complete, or delete tasks, you MUST use the corresponding functions:
- Use createTask() to add new tasks
- Use toggleTaskStatus() to mark tasks as done/undone
- Use deleteTask() to remove tasks

Always include the task ID when toggling or deleting tasks. IDs are shown above.

RESPONSE FORMAT:
- Use **bold** for important information and task names
- Use bullet lists (- ) for multiple items
- Use emojis appropriately (✅ ❌ 📝 ⏰ 🎯 etc.)
- Keep responses clear and well-structured with markdown

GUIDELINES:
- Be encouraging and supportive about task completion
- Provide actionable suggestions
- Keep responses concise but helpful
- When asked about productivity, give practical tips
- Celebrate accomplishments when tasks are completed
- ALWAYS use functions to modify tasks, don't just describe what to do
"""

    # Define tools for function calling
    tools = [
        {
            "type": "function",
            "function": {
                "name": "createTask",
                "description": "Create a new todo task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The task description"
                        }
                    },
                    "required": ["text"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "toggleTaskStatus",
                "description": "Mark a task as done or undone (toggle completion status)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "description": "The ID of the task to toggle"
                        }
                    },
                    "required": ["id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "deleteTask",
                "description": "Delete a task from the list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "description": "The ID of the task to delete"
                        }
                    },
                    "required": ["id"]
                }
            }
        }
    ]

    # Convert message history to LangChain format
    lc_messages = [SystemMessage(content=system_content)]
    
    for msg in messages:
        if msg.role == "user":
            lc_messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            lc_messages.append(AIMessage(content=msg.content))
    
    # Bind tools to model
    model_with_tools = model.bind_tools(tools)
    
    # Get AI response
    response = await model_with_tools.ainvoke(lc_messages)
    
    # Extract actions from tool calls
    result_actions = []
    action_descriptions = []
    
    if hasattr(response, 'tool_calls') and response.tool_calls:
        for tool_call in response.tool_calls:
            action_type = None
            payload = {}
            
            if tool_call['name'] == 'createTask':
                action_type = 'post'
                task_text = tool_call['args'].get('text')
                payload = {'text': task_text}
                action_descriptions.append(f'creada la tarea "{task_text}"')
            elif tool_call['name'] == 'toggleTaskStatus':
                action_type = 'put'
                task_id = tool_call['args'].get('id')
                payload = {'id': task_id}
                # Find the task to get its name
                task = next((t for t in todos if t['id'] == task_id), None)
                if task:
                    status = "completada" if not task.get('done') else "marcada como pendiente"
                    action_descriptions.append(f'{status} la tarea "{task["text"]}"')
                else:
                    action_descriptions.append(f'actualizada la tarea #{task_id}')
            elif tool_call['name'] == 'deleteTask':
                action_type = 'delete'
                task_id = tool_call['args'].get('id')
                payload = {'id': task_id}
                # Find the task to get its name
                task = next((t for t in todos if t['id'] == task_id), None)
                if task:
                    action_descriptions.append(f'eliminada la tarea "{task["text"]}"')
                else:
                    action_descriptions.append(f'eliminada la tarea #{task_id}')
            
            if action_type:
                result_actions.append(Action(type=action_type, payload=payload))
    
    # Generate appropriate response text
    if result_actions:
        # If we have actions, create a friendly confirmation message with markdown
        if len(action_descriptions) == 1:
            response_text = f"✅ **{action_descriptions[0].capitalize()}**"
        else:
            response_text = "✅ **He realizado las siguientes acciones:**\n\n" + "\n".join([f"- {desc}" for desc in action_descriptions])
        
        # Add AI's original message if it provided one
        if response.content:
            response_text = response.content + "\n\n" + response_text
    else:
        # No actions, use AI's response or default
        response_text = response.content or "¡Estoy aquí para ayudarte a gestionar tus tareas! 📝"
    
    return AgentResponse(
        response=response_text,
        actions=result_actions if result_actions else None,
        context=None
    )


# Create and register agent router
router = create_agent_router(
    agent_handler=todo_agent,
    tags=["todo-agent"]
)
app.include_router(router)


@app.get("/")
async def root():
    """API information endpoint"""
    return {
        "message": "Todo Assistant API",
        "version": "0.2.0",
        "model": "{messages, actions, context}",
        "description": "AI-powered task management assistant using agent-state-bridge",
        "endpoints": {
            "/chat": "POST - Chat with the todo assistant",
            "/docs": "GET - API documentation"
        }
    }


def main():
    """Run the development server"""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "agent:app",
        host="0.0.0.0",
        port=port,
        reload=True,
    )


if __name__ == "__main__":
    main()
