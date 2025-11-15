"""
Shopping Assistant Agent using agent-state-bridge with {messages, actions, context} model

This example demonstrates:
- Separating CRUD operations (actions) from state (context)
- Using LangChain for AI responses
- RAG-ready architecture (context can include vector search results)
- Bidirectional actions (agent can return actions for frontend to execute)
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
app = FastAPI(title="Shopping Assistant API")

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


async def shopping_agent(
    messages: List[Message], 
    actions: List[Action], 
    context: Dict[str, Any]
) -> AgentResponse:
    """
    Shopping assistant agent handler.
    
    Args:
        messages: Conversation history with user
        actions: Recent CRUD operations on the cart (optional, for context)
        context: Current application state including:
            - products: Available products catalog
            - cart: Current cart state (items, total, itemCount)
            - (future) ragResults: Vector search results for RAG
    
    Returns:
        AgentResponse containing:
            - response: Agent's text response
            - actions: Optional list of actions for frontend to execute
            - context: Optional updated context
    """
    
    # Extract context data
    cart_items = context.get('cart', {}).get('items', [])
    products = context.get('products', [])
    cart_total = context.get('cart', {}).get('total', 0)
    
    # Build cart summary for system prompt
    if cart_items:
        cart_summary = "\n".join([
            f"- {item['name']} x{item['quantity']} (${item['price']:.2f} each) = ${item['price'] * item['quantity']:.2f}" 
            for item in cart_items
        ])
    else:
        cart_summary = "Cart is empty"
    
    # Build recent actions context (if any)
    actions_context = ""
    if actions:
        actions_context = "\n\nRECENT USER ACTIONS:\n" + "\n".join([
            f"- {action.type}: {action.payload}" for action in actions
        ])
    
    # Build comprehensive system prompt
    system_content = f"""You are an expert shopping assistant for a dessert store.

CURRENT CART STATE:
{cart_summary}
Total items: {len(cart_items)}
Total price: ${cart_total:.2f}

AVAILABLE PRODUCTS:
{chr(10).join([f"- {p['name']} ({p.get('category', 'N/A')}) - ${p.get('price', 0):.2f}" for p in products])}
{actions_context}

YOUR CAPABILITIES:
1. Answer questions about products and pricing
2. Help users find products by category or description
3. Provide cart summaries and calculations
4. Suggest products based on user preferences
5. (Optional) You can return actions for the frontend to execute:
   - type: 'post' with payload: {{"productName": "..."}} to add a product
   - type: 'put' with payload: {{"productName": "...", "quantity": N}} to update quantity
   - type: 'delete' with payload: {{"productName": "..."}} to remove a product

GUIDELINES:
- Be conversational, friendly, and helpful
- When suggesting products, provide clear reasons
- If asked about the cart, provide detailed information
- Keep responses concise but informative
- Currently, actions are suggestions only (frontend executes them)
"""

    # Convert message history to LangChain format
    lc_messages = [SystemMessage(content=system_content)]
    
    for msg in messages:
        if msg.role == "user":
            lc_messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            lc_messages.append(AIMessage(content=msg.content))
    
    # Get AI response
    response = await model.ainvoke(lc_messages)
    response_text = response.content or "I'm here to help with your shopping!"
    
    # Future enhancement: Parse response or use function calling to detect desired actions
    # For now, we return text-only responses
    # Example with function calling:
    # if agent_wants_to_add_product:
    #     return AgentResponse(
    #         response=response_text,
    #         actions=[Action(type="post", payload={"productName": "Waffle"})],
    #         context=None
    #     )
    
    return AgentResponse(
        response=response_text,
        actions=None,  # Could return actions for frontend to execute
        context=None   # Could return updated context (e.g., RAG results)
    )


# Create and register agent router
router = create_agent_router(
    agent_handler=shopping_agent,
    tags=["shopping-agent"]
)
app.include_router(router)


@app.get("/")
async def root():
    """API information endpoint"""
    return {
        "message": "Shopping Assistant API",
        "version": "0.2.0",
        "model": "{messages, actions, context}",
        "description": "AI-powered shopping assistant using agent-state-bridge",
        "endpoints": {
            "/chat": "POST - Chat with the shopping assistant",
            "/docs": "GET - API documentation"
        }
    }


def main():
    """Run the development server"""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "agent:app",  # Assuming this file is named agent.py
        host="0.0.0.0",
        port=port,
        reload=True,
    )


if __name__ == "__main__":
    main()
