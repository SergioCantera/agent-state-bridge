import { useAgentChat } from 'agent-state-bridge';
import { useCartStore } from './cart.store';
import productsData from './products.json'; // Your products catalog

/**
 * Custom hook using agent-state-bridge with {messages, actions, context} model
 * 
 * Demonstrates:
 * - Separating CRUD operations (actions) from state (context)
 * - Preparing context for RAG integration
 * - Handling bidirectional actions from agent
 */
export const useShoppingAgentChat = () => {
  const { cartItems, totalOrder, addProduct, updateQuantity, deleteProduct } = useCartStore();

  const { messages, sendMessage, loading, error } = useAgentChat({
    endpoint: 'http://localhost:8000/chat',
    
    // Context: Current app state + data (RAG-ready)
    // This is where you could add vector search results
    getContext: () => ({
      products: productsData.map(p => ({ 
        name: p.name, 
        category: p.category, 
        price: p.price 
      })),
      cart: {
        items: cartItems,
        total: totalOrder(),
        itemCount: cartItems.length
      }
      // Future: Add RAG data here
      // ragResults: vectorStore.similaritySearch(lastMessage)
    }),
    
    // Actions: Recent state mutations (optional, for agent context)
    getActions: () => {
      // You could track recent user actions here
      // Example: [{type: 'post', payload: {productName: 'Waffle'}}]
      return [];
    },
    
    // Callback: Handle actions returned by the agent
    onActionsReceived: (actions) => {
      actions.forEach(action => {
        switch (action.type) {
          case 'post':
            // Add product to cart
            if (action.payload?.productName) {
              const product = productsData.find(p => 
                p.name.toLowerCase().includes(action.payload.productName.toLowerCase())
              );
              if (product) addProduct(product);
            }
            break;
            
          case 'put':
            // Update quantity
            if (action.payload?.productName && action.payload?.quantity) {
              const product = cartItems.find(p => 
                p.name.toLowerCase().includes(action.payload.productName.toLowerCase())
              );
              if (product) updateQuantity(product.name, action.payload.quantity);
            }
            break;
            
          case 'delete':
            // Remove from cart
            if (action.payload?.productName) {
              const product = cartItems.find(p => 
                p.name.toLowerCase().includes(action.payload.productName.toLowerCase())
              );
              if (product) deleteProduct(product.name);
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
