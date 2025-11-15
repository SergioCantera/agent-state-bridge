"""
Example: Simple agent with Flask
"""
from flask import Flask
from agent_state_bridge.flask import create_agent_blueprint


def simple_agent(message: str, state: dict) -> str:
    """Simple echo agent"""
    cart_items = state.get("cart", {}).get("items", [])
    return f"You said: '{message}'. You have {len(cart_items)} items in cart."


# Create Flask app
app = Flask(__name__)

# Register agent blueprint
bp = create_agent_blueprint(simple_agent)
app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
