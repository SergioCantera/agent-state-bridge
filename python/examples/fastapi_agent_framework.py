"""
Example: Using agent-state-bridge with Microsoft Agent Framework and FastAPI
"""
from fastapi import FastAPI
from agent_state_bridge.fastapi import create_agent_router

# Example using Microsoft Agent Framework
try:
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import AgentMessage
    from azure.identity import DefaultAzureCredential
except ImportError:
    print("Install: pip install azure-ai-projects azure-identity")
    raise


# Initialize Azure AI Project Client
# Note: Requires AZURE_AI_PROJECT_CONNECTION_STRING or endpoint/key
project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="<your-endpoint>"
)

# Create agent
agent = project_client.agents.create_agent(
    model="gpt-4o-mini",
    instructions="You are a helpful shopping assistant."
)


async def agent_framework_handler(message: str, state: dict) -> str:
    """Process message using Microsoft Agent Framework"""
    # Create thread
    thread = project_client.agents.create_thread()
    
    # Add context from state
    cart_items = state.get("cart", {}).get("items", [])
    context_msg = f"Current cart has {len(cart_items)} items."
    
    # Send messages
    project_client.agents.create_message(
        thread_id=thread.id,
        content=context_msg,
        role="user"
    )
    project_client.agents.create_message(
        thread_id=thread.id,
        content=message,
        role="user"
    )
    
    # Run agent
    run = project_client.agents.create_run(
        thread_id=thread.id,
        assistant_id=agent.id
    )
    
    # Wait for completion
    while run.status in ["queued", "in_progress"]:
        run = project_client.agents.get_run(thread_id=thread.id, run_id=run.id)
    
    # Get response
    messages = project_client.agents.list_messages(thread_id=thread.id)
    return messages.data[0].content[0].text.value


# Create FastAPI app
app = FastAPI(title="Agent Framework Example")

# Add agent router
router = create_agent_router(agent_framework_handler, tags=["agent-framework"])
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
