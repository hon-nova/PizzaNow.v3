
import type { Pizza } from "../shared/types"
import { useState } from "react"
// import { useCartStore } from "../stores/cartStore"

type PizzaCartState = {
   pizza: Pizza,
   addToCart: (item:Pizza,unit_type:string)=>void
}

export const PizzaCard = ({ pizza, addToCart }: PizzaCartState) => {
 
   const [ selectedUnitType, setSelectedUnitType ]= useState<string>("slice")

   // console.log(`current selectedUnitType: ${selectedUnitType}`)
   // const { setType } = useCartStore()
   function handleAddToCart(e:React.FormEvent<HTMLFormElement>){
      e.preventDefault()
      addToCart(pizza,selectedUnitType)
   }
  return (
    <div className="bg-white shadow rounded overflow-hidden flex flex-col sm:flex-row">
      {/* Left Column - Image */}
      <div className="sm:w-1/2 w-full">
         <img
            src={pizza.image_url}
            alt={pizza.name}
            className="w-full h-[360px] object-cover" />
      </div>
      {/* Right Column - Info */}
      <div className="sm:w-1/2 w-full p-4 flex flex-col justify-between">
        <div>
          <h2 className="text-xl font-semibold text-black mb-2 text-center">{pizza.name} </h2>
           <h2 className="text-xl font-semibold text-black mb-2 text-center">${pizza.slice_price}/slice </h2>
          <p className="text-sm text-gray-600 mb-4">{pizza.description}</p>
          <ul>
            {pizza?.ingredients && 
            pizza.ingredients.map((item)=>(
               <li key={item}>{item}</li>
            ))}
          </ul>         
        </div>
        {/* setType: (pizza:Pizza,type:string) */}
        <div className="flex flex-row mx-auto space-x-4">
            <form action="" onSubmit={handleAddToCart}>
               <select 
                  value={selectedUnitType}
                  onChange={(e)=>{
                     setSelectedUnitType(e.target.value)   // update local
                     
                  }}
                  className="border-2 border-dashed rounded">
                  <option value="slice">Slice</option>
                  <option value="full">Full Unit</option>
               </select>
                <button
                  className="bg-amber-500 text-white px-4 py-2 w-[140px] rounded-lg hover:bg-amber-700 transition"
                  >Add to Cart</button>  
            </form>          
            
        </div>        
      </div>
    </div>
  )
}