"""FastAPI integration for agent-state-bridge"""
from typing import Callable, Awaitable
from fastapi import APIRouter
from .models import AgentRequest, AgentResponse


def create_agent_router(
    agent_handler: Callable[[str, dict], Awaitable[str]],
    prefix: str = "",
    tags: list[str] = None
) -> APIRouter:
    """
    Create a FastAPI router with agent chat endpoint.
    
    Args:
        agent_handler: Async function that takes (message, state) and returns response string
        prefix: Router prefix (default: "")
        tags: Router tags for OpenAPI docs
        
    Returns:
        FastAPI APIRouter with /chat endpoint
        
    Example:
        ```python
        from fastapi import FastAPI
        from agent_state_bridge.fastapi import create_agent_router
        
        async def my_agent(message: str, state: dict) -> str:
            # Your agent logic here
            return f"Processed: {message}"
        
        app = FastAPI()
        router = create_agent_router(my_agent, tags=["agent"])
        app.include_router(router)
        ```
    """
    router = APIRouter(prefix=prefix, tags=tags or ["agent"])
    
    @router.post("/chat", response_model=AgentResponse)
    async def chat_endpoint(request: AgentRequest) -> AgentResponse:
        """Agent chat endpoint"""
        response = await agent_handler(request.message, request.state)
        return AgentResponse(response=response)
    
    return router


# Alternative: Decorator-based approach
class AgentBridge:
    """
    Class-based approach for FastAPI integration.
    
    Example:
        ```python
        from fastapi import FastAPI
        from agent_state_bridge.fastapi import AgentBridge
        
        app = FastAPI()
        bridge = AgentBridge(app)
        
        @bridge.agent_handler
        async def my_agent(message: str, state: dict) -> str:
            return f"Got: {message}"
        ```
    """
    
    def __init__(self, app=None, prefix: str = "", tags: list[str] = None):
        self.prefix = prefix
        self.tags = tags or ["agent"]
        self._handler = None
        if app:
            self.init_app(app)
    
    def agent_handler(self, func: Callable[[str, dict], Awaitable[str]]):
        """Decorator to register agent handler"""
        self._handler = func
        return func
    
    def init_app(self, app):
        """Initialize with FastAPI app"""
        if not self._handler:
            raise ValueError("No agent handler registered. Use @bridge.agent_handler decorator")
        
        router = create_agent_router(self._handler, self.prefix, self.tags)
        app.include_router(router)
