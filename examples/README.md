# Examples

This directory contains example projects demonstrating how to use `agent-state-bridge` in real-world applications.

## Available Examples

### 1. Shopping Cart ([shopping-cart/](./shopping-cart/))

**Full-stack AI-powered shopping assistant**

- **Frontend**: React + Vite + Zustand
- **Backend**: Python + FastAPI + LangChain
- **Features**: 
  - Chat with AI about products
  - AI understands full cart context
  - Bidirectional actions (agent can suggest cart operations)
  - RAG-ready architecture

**Key learning points:**
- Using `{messages, actions, context}` model
- Separating CRUD operations from state
- Handling agent actions in frontend
- LangChain integration

[View Example →](./shopping-cart/)

---

## Running the Examples

Each example has its own README with setup instructions. Generally:

**Backend:**
```bash
cd <example>/backend
pip install -r requirements.txt
# Configure .env file
python agent.py
```

**Frontend:**
```bash
cd <example>/frontend
npm install
npm run dev
```

## Contributing Examples

Have a cool example using `agent-state-bridge`? We'd love to include it!

1. Create a directory under `examples/`
2. Include both frontend and backend code
3. Add a comprehensive README
4. Document the key concepts demonstrated
5. Submit a PR

## Example Ideas

Here are some example ideas we'd love to see:

- **Todo List with AI**: Task management with AI suggestions
- **Document Chat**: RAG-based document Q&A
- **E-commerce Recommender**: Product recommendations using vector search
- **Multi-agent Workflow**: Multiple agents collaborating
- **Real-time Dashboard**: AI analyzing live data streams
- **Code Assistant**: AI helping with coding tasks

## Need Help?

- [Main Documentation](../README.md)
- [API Reference](../README.md#-api-reference)
- [Architecture Guide](../ARQUITECTURA_ESTADO.md)
- [GitHub Issues](https://github.com/SergioCantera/agent-state-bridge/issues)
