"""
Example: Using agent-state-bridge with LangChain and FastAPI
"""
from fastapi import FastAPI
from agent_state_bridge.fastapi import create_agent_router

# Example using LangChain
try:
    from langchain_openai import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
except ImportError:
    print("Install langchain: pip install langchain langchain-openai")
    raise


# Initialize LangChain model
llm = ChatOpenAI(model="gpt-4o-mini")


async def langchain_agent(message: str, state: dict) -> str:
    """Process message using LangChain"""
    # Build context from state
    cart_items = state.get("cart", {}).get("items", [])
    context = f"User has {len(cart_items)} items in cart."
    
    messages = [
        SystemMessage(content=f"You are a shopping assistant. Context: {context}"),
        HumanMessage(content=message)
    ]
    
    response = await llm.ainvoke(messages)
    return response.content


# Create FastAPI app
app = FastAPI(title="LangChain Agent Example")

# Add agent router
router = create_agent_router(langchain_agent, tags=["langchain"])
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
