import { Link } from "react-router-dom"
import { useUserStore } from "../stores/userStore"
import { useCartStore } from "../stores/cartStore"
import { useEffect } from "react"

export function Cart(){
   const { user } = useUserStore()
   const { cart, setUserId, updateCartItem, removeFromCart} = useCartStore()
   const userId = user?.id
   const cartItems = cart?.cartItems
   // console.log(`current user id: ${userId}`)
   // console.log(`cartItems: ${JSON.stringify(cartItems)}`)
   function displayCartItems(){
      cartItems.map((item,index)=>{
         console.log(`< =========item ${index}`)
         console.log(`name: ${item.pizza.name}; type: ${item.unit_type}: Qty:${item.quantity} -> ${item.subAmount}=========== >`)
        
      })
   }
   displayCartItems()
  
   useEffect(()=>{
      if (userId){
         setUserId(userId)
      }
   },[setUserId,userId])

   return (
      <div className="grid grid-cols-12 gap-2 py-2 h-screen">
         <div className="col-span-8 bg-amber-100">
            <p>Your cart: {cart?.totalItem} items</p>
            {cartItems.map((pizzaItem)=>(
               <div className="grid grid-cols-5 bg-white rounded my-1 py-2" key={pizzaItem.pizza.name}>
                  <div className="flex flex-row col-span-3 border rounded py-2">left
                     <img src={pizzaItem.pizza.image_url} alt="pizza" className="h-[150px] w-[180px] p-2 rounded-2xl border" object-cover="true" />
                     <ul className="ml-3">
                        <li className="font-bold">{pizzaItem.pizza.name}</li>
                        <li className="italic">{pizzaItem.pizza.description?.substring(0,30)}...</li>
                        <li className="flex justify-between">                        
                           <span className="flex font-bold p-2 bg-yellow-100 items-end">$ {pizzaItem.pizza.slice_price}/slice</span>
                           <span className="font-bold p-2 bg-green-100">$ {pizzaItem.pizza.full_price}/full unit</span>
                        </li>                        
                        <li className="mt-2">SHIPPING | PICKUP TODAY</li>
                     </ul>
                  </div>
                  {/* <div className="">middle</div> */}
                  <div className="flex flex-col col-span-2 items-end border rounded">
                     <div className="flex flex-row flex-shrink-0 w-full h-[20px] justify-between">
                        <div className="flex flex-row items-center mx-auto">
                           <p>Qty </p>
                           <select
                              value={pizzaItem.quantity}
                              onChange={(e)=>updateCartItem(pizzaItem,Number(e.target.value),pizzaItem.unit_type)}>                     
                           {[1,2,3,4,5,6,7,8,9].map((item=>(
                              <option key={item}>{item}</option>
                           )))}                    
                           </select>
                        </div>
                        <div className="flex flex-row items-center mx-auto">
                           <p>Type</p>
                           <select
                              value={pizzaItem.unit_type}
                              onChange={(e)=>updateCartItem(pizzaItem,pizzaItem.quantity,e.target.value)}>                      
                           {["slice","full"].map((item=>(
                              <option key={item}>{item}</option>
                           )))}                    
                           </select>
                        </div>
                       
                     </div> 
                     {/* <div className="flex flex-row flex-shrink-0 w-[120px] h-[20px] items-center">
                       
                     </div>                   */}
                     <div className="mt-auto">
                        <button 
                           onClick={()=>removeFromCart(pizzaItem)}
                           className="border border-blue-300 p-3 rounded cursor-pointer">Remove</button>
                     </div>                 
                  </div>
            </div>
            ))}
           
         </div>
         <div className="col-span-4 bg-pink-100 border-left">
           <Link to="/pay" className="rounded-lg font-bold p-2 border">Pay with PayPal</Link>
         </div>
      </div>
   )
}