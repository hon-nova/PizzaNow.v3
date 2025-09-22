// import { create } from "zustand"
// import { persist, createJSONStorage } from "zustand/middleware"
// import type { Item,  Cart, Pizza } from "../shared/types"
// import { useUserStore } from "./userStore"
// // import { useUserStore } from "./userStore"


// const BASE_URL= import.meta.env.VITE_BACKEND_URL
// console.log(`@zustand: BASE_URL`, BASE_URL)
// // const { user } = useUserStore.getState()
// type CartState = {
//    cart: Cart 
// }
// type CartActions ={   
//    setCart: (cart:Cart) =>void
//    addToCart: (pizza: Pizza,unit_type:string)=>void
//    updateCartItem: (updatedItem: Item,quantity:number,unit_type:string)=>void
//    removeFromCart: (item:Item)=>void
//    clearCart: ()=>void
//    setUserId:(userId:string)=>void
// }

// const calculateTotals = (items: Item[], shippingFee: number, discount: number) => {
//   const subTotal = items.reduce((acc, { subAmount }) => acc + subAmount, 0)
//   const taxes = subTotal * 0.12
//   const total = subTotal + taxes + shippingFee - discount
//   const totalItem = items.reduce((acc, { quantity })=> acc + quantity,0)
//   return { subTotal, taxes, total, totalItem }
// }

// export const useCartStore = create<CartState & CartActions>()(
//   persist((set,get) => ({
//       cart: {
//          userId: '',
//          cartItems:[],
//          subTotal: 0,
//          taxes: 0,
//          shippingFee: 6.99,
//          discount: 10,
//          total:0.0,
//          totalItem:0
//       },
     
//       setCart:(cart)=>{
//          const { user } = useUserStore.getState()
//          if (!user?.id) return

//          const cartWithUserId = {...cart, userId: user.id}
//          set({cart: cartWithUserId})
         
//          // also save to user-specific localStorage
//          localStorage.setItem(`cart-storage-${cart.userId}`, JSON.stringify({ cart }));
         
         
//       },
//       addToCart: (newPizza:Pizza, unit_type:string)=>{
//          const u_type = unit_type as 'slice' | 'full'
//          const cart = get().cart
//          let updatedCartItems = get().cart.cartItems.slice()
         
//          const existingItemIndex = updatedCartItems.findIndex((item:Item)=>item.pizza.id === newPizza.id)
         
//          if (existingItemIndex  === -1){
//             const newItem: Item = {
//                pizza: newPizza, 
//                quantity: 1,
//                unit_type: u_type,
//                subAmount : (u_type==='full') ? (newPizza.full_price) : (newPizza.slice_price) 
//             }
//             updatedCartItems = [...updatedCartItems,newItem]
            
//          }        
//          else {
//             const existingItem = updatedCartItems[existingItemIndex]
//             const updatedItem = {
//                ...existingItem,
//                quantity: existingItem.quantity +1,
//                unit_type: u_type,
//                subAmount: (u_type==='full')? (newPizza.full_price*(existingItem.quantity +1)): (newPizza.slice_price*(existingItem.quantity +1))
//             }
//             updatedCartItems[existingItemIndex] = updatedItem
            
//          }
//          // update
//          const { subTotal, taxes, total, totalItem  } = calculateTotals (updatedCartItems, cart.shippingFee, cart.discount)

//          set({cart: {...cart, cartItems: updatedCartItems,subTotal:Number(subTotal),taxes,total, totalItem}})         
        
//       },
//       updateCartItem: (updatedItem: Item,quantity:number,unit_type:string)=>{
//       const u_type = unit_type as 'slice'|'full'
//       const cart = get().cart
//       let updatedCartItems = cart.cartItems.slice()
//       const itemToUpdate = updatedCartItems.find((item:Item)=>item.pizza.id === updatedItem.pizza.id)
//       if (itemToUpdate){
//          updatedCartItems =[
//             ...updatedCartItems,
//             {...itemToUpdate,
//                quantity:quantity,
//                unit_type: u_type,
//                subAmount: (u_type==='full')? (quantity*updatedItem.pizza.full_price):(quantity*updatedItem.pizza.slice_price)}]
//       }
   
//        const { subTotal, taxes, total, totalItem } = calculateTotals (updatedCartItems, cart.shippingFee, cart.discount)

//       set({cart: {...get().cart, cartItems: updatedCartItems,subTotal,taxes,total, totalItem}})
//       },
//       removeFromCart: (removedItem:Item)=> {
//          const cart = get().cart
//          const updatedCartItems = cart.cartItems.slice().filter((item:Item)=>item.pizza.id !==removedItem.pizza.id)

//          const { subTotal, taxes, total  } = calculateTotals (updatedCartItems, cart.shippingFee, cart.discount)
//          set({cart: {...cart, cartItems: updatedCartItems, subTotal, taxes, total}})
        
//       },
//       clearCart: ()=>{
//          const cart = get().cart
         
//          set({cart: {...cart,cartItems:[], subTotal:0,taxes:0,shippingFee:0,discount:0,total:0,userId:cart.userId, totalItem:0 }})
//       },
//       setUserId:(userId:string)=>{                
         
//          const stored = localStorage.getItem(`cart-storage-${userId}`);
//          if (stored ) {
//             const parsed = JSON.parse(stored)            
//             set({cart: {...(parsed.cart),userId}})         
//          } else {
//             // reset empty cart for new user
//             set({ cart: { userId, cartItems: [], subTotal: 0, taxes: 0, shippingFee: 0, discount: 0, total: 0, totalItem: 0 } })
//             }
//       },

//    }), {
//       name:`cart-storage`,
//       storage: createJSONStorage(() => localStorage),
//       partialize: (state) => ({ cart: state.cart })
//     })
//    )

// // function setItem(userId: string, key: string, value:string) {
// //   localStorage.setItem(`${userId}:${key}`, JSON.stringify(value));
// // }

// // function getItem(userId: string, key: string) {
// //   const raw = localStorage.getItem(`${userId}:${key}`);
// //   return raw ? JSON.parse(raw) : null;
// // }

// // function clearUser(userId: string) {
// //   Object.keys(localStorage).forEach(k => {
// //     if (k.startsWith(userId + ":")) localStorage.removeItem(k);
// //   });
// // }
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
   shippingFee: 6.99,
   discount: 10,
   total: 0,
   totalItem: 0,
})

const calculateTotals = (items: Item[], shippingFee: number, discount: number) => {
   const subTotal = items.reduce((acc, { subAmount }) => Number(acc + subAmount), 0)
   const taxes = Number(subTotal * 0.12)
   const total = Number(subTotal + taxes + shippingFee - discount)
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








