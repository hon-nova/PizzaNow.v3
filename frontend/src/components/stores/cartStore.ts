import { create } from "zustand"
import type { Item, Cart, Pizza } from "../shared/types"
import { useUserStore } from "./userStore"

type CartState = {
  cart: Cart
}

type CartActions = {
   setCart: (cart: Cart) => void
   addToCart: (pizza: Pizza, unit_type: string) => void
   updateCartItem: (updatedItem: Item, quantity: number, unit_type: string) => void

   removeFromCart: (item: Item) => void
   clearCart: () => void
   setUserId: (userId: string) => void
   setType: (pizza: Pizza,type:string) =>void
}

const emptyCart = (userId: string): Cart => ({
   userId,
   cartItems: [],
   subTotal: 0,
   taxes: 0,
   shippingFee: 3.99,
   discount: 10,
   total: 0,
   totalItem: 0,
})

const calculateTotals = (items: Item[], shippingFee: number, discount: number) => {
   const subTotal = items.reduce((acc, { subAmount }) => Number(acc + subAmount), 0)
   const taxes = Number((subTotal * 0.05))
   const total = Number((subTotal + taxes + shippingFee - discount))
   const totalItem = items.reduce((acc, { quantity }) => Number(acc + quantity), 0)
   return { subTotal, taxes, total, totalItem }
}

export const useCartStore = create<CartState & CartActions>((set, get) => ({
   cart: emptyCart(""),

   setCart: (cart) => {
      const { user } = useUserStore.getState()
      if (!user?.id) return

      const cartWithUser = { ...cart, userId: user.id }
      set({ cart: cartWithUser })
      localStorage.setItem(`cart-storage-${user.id}`, JSON.stringify({ cart: cartWithUser }))
   },

   addToCart: (pizza, type) => {
      const cart = get().cart
      const updatedCartItems = [...cart.cartItems]
      const idx = updatedCartItems.findIndex((item) => item.pizza.id === pizza.id)

      if (idx === -1) {
         updatedCartItems.push({
         pizza,
         quantity: 1,
         unit_type:type,
         subAmount: type === "full" ? Number(pizza.full_price) : Number(pizza.slice_price),
         })
      } else {
         const existing = updatedCartItems[idx]
         updatedCartItems[idx] = {
         ...existing,
         quantity: existing.quantity + 1,
         unit_type:type,
         subAmount:
            type === "full"
               ? Number(pizza.full_price * (existing.quantity + 1))
               : Number(pizza.slice_price * (existing.quantity + 1)),
         }
      }
      const { subTotal, taxes, total, totalItem } = calculateTotals(
         updatedCartItems,
         cart.shippingFee,
         cart.discount
      )

      const updatedCart = { ...cart, cartItems: updatedCartItems, subTotal, taxes, total, totalItem }
      get().setCart(updatedCart)
   },

   updateCartItem: (updatedItem, quantity, unit_type) => {
      const cart = get().cart
      const updatedCartItems = cart.cartItems.map((item) =>
         item.pizza.id === updatedItem.pizza.id
         ? {
               ...item,
               quantity,
               unit_type,
               subAmount:
               unit_type === "full"
                  ? Number(quantity * updatedItem.pizza.full_price)
                  : Number(quantity * updatedItem.pizza.slice_price),
            }
         : item
      )

      const { subTotal, taxes, total, totalItem } = calculateTotals(
         updatedCartItems,
         cart.shippingFee,
         cart.discount
      )

      const updatedCart = { ...cart, cartItems: updatedCartItems, subTotal, taxes, total, totalItem }
      get().setCart(updatedCart)
   },

   removeFromCart: (removedItem) => {
         const cart = get().cart
         const updatedCartItems = cart.cartItems.filter((i) => i.pizza.id !== removedItem.pizza.id)
         const { subTotal, taxes, total, totalItem } = calculateTotals(
            updatedCartItems,
            cart.shippingFee,
            cart.discount
         )
         const updatedCart = { ...cart, cartItems: updatedCartItems, subTotal, taxes, total, totalItem }
         get().setCart(updatedCart)
         
         // alert(`remove item name: ${removedItem.pizza.name}`)
   },

   clearCart: () => {
      const { user } = useUserStore.getState()
      if (!user?.id) return
      const cleared = emptyCart(user.id)
      set({ cart: cleared })
      localStorage.setItem(`cart-storage-${user.id}`, JSON.stringify({ cart: cleared }))
   },

   setUserId: (userId) => {
      const stored = localStorage.getItem(`cart-storage-${userId}`)
      if (stored) {
         const parsed = JSON.parse(stored)
         set({ cart: { ...parsed.cart, userId } })
      } else {
         set({ cart: emptyCart(userId) })
      }
   },
   setType: (pizza:Pizza,type:string)=>{
      const cart = get().cart
      
      const updatedCartItems = cart.cartItems.map((item)=> item.pizza.id === pizza.id ? ({...item, unit_type:type}):item)
      const { subTotal, taxes, total, totalItem } = calculateTotals(
            updatedCartItems,
            cart.shippingFee,
            cart.discount
         )

      const updatedCart = { ...cart, cartItems: updatedCartItems, subTotal, taxes, total, totalItem }
      alert(`setType now: ${type}`)
      console.log(`cart: `,JSON.stringify(get().cart))
      get().setCart(updatedCart)
   }
}))








