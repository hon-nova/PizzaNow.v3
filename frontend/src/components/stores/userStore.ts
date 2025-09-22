
import { create } from 'zustand'
import { persist,createJSONStorage } from 'zustand/middleware'
// import { useCartStore } from './cartStore'

import type { User } from '../shared/types'

type UserState = {
   user: User|null
   setUser: (u:User) =>void
   // loginSuccess: (user: User)=>void
   logout: ()=>void
  
}
export const useUserStore = create<UserState>()(
   persist (
      (set)=>({
         user: null,
         setUser: (userData)=>set({user: userData }),
         // loginSuccess:(user)=>{
         //    const { cart, clearCart, setUserId } = useCartStore.getState()
         //    if(user?.id && cart.userId !== user.id){
         //       clearCart()
         //       setUserId(user.id)
         //    }
         //    set({user})
         // },
         logout: async () => {
            try {
               await fetch(`${import.meta.env.VITE_BACKEND_URL}/auth/logout`, {
                  method: "POST",
                  credentials: "include", 
               });
            } catch (err) {
               console.error("Failed to logout from backend:", err);
            }
            set({ user: null }); }
      }), 
      {
         name:"user-storage",
         storage: createJSONStorage(() => localStorage)
      },
   )
)