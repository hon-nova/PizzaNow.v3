import { create } from 'zustand'
import { persist,createJSONStorage } from 'zustand/middleware'

import type { User } from '../shared/types'

type UserState = {
   user: User|null
   setUser: (u:User) =>void
   logout: ()=>void
  
}
export const useUserStore = create<UserState>()(
   persist (
      (set)=>({
         user: null,
         setUser: (userData)=>set({user: userData }),
         
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