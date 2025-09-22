import { useEffect } from "react"
import { PizzaCard } from "./PizzaCard"
import { Footer } from "./Footer"
import { usePizzaStore } from "../stores/pizzaStore"
import { useCartStore } from "../stores/cartStore"
// import { useUserStore } from "../stores/userStore"

export function PizzaStore() {
   
   const { pizzas, page, totalPages, setPage} = usePizzaStore()
   
   // const { user} = useUserStore()
   // const userId = user?.id ? user?.id : "no_user_id_pizzastore"

   const { addToCart } = useCartStore();
   
  //no arg 'userId'

   useEffect(() => {
      setPage(1);
      }, [setPage])

   return (
    <div className="bg-[#f5f5f5] min-h-screen pt-6 ">
      <h1 className="text-3xl font-bold text-black mb-6 ">Pizza Store</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mx-20">
        {pizzas.map((pizza,index) => (
         <div key={index} className="border border-gray-300 rounded-lg p-4">
             <PizzaCard pizza={pizza} addToCart={()=>addToCart(pizza,"slice")}/>
         </div>         
        ))}
      </div>
      {/* TODO: Add Pagination Controls Here */}         
      <div className="flex justify-center mt-4">
         <button 
            disabled={page === 1} 
            onClick={() => setPage(page - 1)}
            className="bg-amber-600 p-2 rounded cursor-pointer">Previous</button>
         <span className="flex flex-row justify-center items-center align-items-center mx-4">| Page {page} of {totalPages} | </span>
         <button 
            disabled={page === totalPages} 
            onClick={() => setPage(page + 1)}
            className="bg-amber-600 p-2 rounded cursor-pointer">Next</button>
      </div>   
      <div><Footer /></div>
    </div>
  )
}