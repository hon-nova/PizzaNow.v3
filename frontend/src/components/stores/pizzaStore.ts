import { create } from "zustand"
// import { persist, createJSONStorage } from "zustand/middleware"
import type { Pizza } from "../shared/types"

type PizzaState = {
  pizzas: Pizza[]
  loading: boolean
  error: string | null
  page: number
  limit: number
  total: number
  totalPages: number
  fetchPizzas: (page: number,limit:number) => Promise<void>  
  setPage: (page: number) => void;
}
const BASE_URL= import.meta.env.VITE_BOT_BACKEND_URL
export const usePizzaStore = create<PizzaState>(  
    (set,get) => ({
      pizzas: [],
      loading: false,
      error: null,
      page:1,
      limit: 8,
      total: 1,
      totalPages:0,      
      fetchPizzas: async (page =get().page, limit=get().limit) => {
                 
         set({ loading: true, error: null })
         try {           
            const res = await fetch(`${BASE_URL}/api/bot/pizzas?page=${page}&limit=${limit}`);
            const data = await res.json();
            set({ 
               pizzas: data.pizzas,
               page: data.page,
               limit: data.limit,
               total: data.total,
               totalPages: data.pages,
             })
         } catch (err) {
               if(err instanceof Error){
                  set({ error: err.message })
               }
         
        } finally {
          set({ loading: false })
        }
      },
      setPage: (page: number) =>{
         set({ page });
         get().fetchPizzas(page, get().limit);
      }      
    })
    
  )

