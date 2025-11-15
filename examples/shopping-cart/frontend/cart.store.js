import { create } from 'zustand';

/**
 * Zustand store for cart management
 * 
 * This store is shared with the AI agent through the context parameter
 */
export const useCartStore = create((set, get) => ({
  cartItems: [],
  
  // Add product to cart
  addProduct: (product) => set((state) => {
    const existing = state.cartItems.find(item => item.name === product.name);
    if (existing) {
      return {
        cartItems: state.cartItems.map(item =>
          item.name === product.name
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      };
    }
    return {
      cartItems: [...state.cartItems, { ...product, quantity: 1 }]
    };
  }),
  
  // Update quantity
  updateQuantity: (productName, quantity) => set((state) => ({
    cartItems: state.cartItems.map(item =>
      item.name === productName
        ? { ...item, quantity: Math.max(1, quantity) }
        : item
    )
  })),
  
  // Remove product
  deleteProduct: (productName) => set((state) => ({
    cartItems: state.cartItems.filter(item => item.name !== productName)
  })),
  
  // Calculate total
  totalOrder: () => {
    return get().cartItems.reduce((acc, item) => acc + (item.quantity * item.price), 0);
  },
  
  // Clear cart
  clearCart: () => set({ cartItems: [] })
}));
