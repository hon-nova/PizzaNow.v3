import { Link } from "react-router-dom"
import { useUserStore } from "../stores/userStore"
import { useCartStore } from "../stores/cartStore"
import { useEffect } from "react"
import { CartNav } from "./CartNav"

export function Cart(){
   // const { user } = useUserStore()   

   const { user, setUser  } = useUserStore()
   const { cart, setUserId, updateCartItem, removeFromCart} = useCartStore()
   const userId = user?.id
   const cartItems = cart?.cartItems
   console.log(`logged-in user: `, user )
  
   const BASE_URL = import.meta.env.VITE_PAYPAL_BACKEND_URL
   
   console.log(`Initial BASE_URL: ${BASE_URL}`) 
   // console.log(`current user id: ${userId}`)
   // console.log(`cartItems: ${JSON.stringify(cartItems)}`)
   useEffect(()=>{
      async function getUser(){
         const res = await fetch(`${BASE_URL}/api/paypal/auth`,{
            method:"GET",
            headers:{
                  "Content-Type":"application/json",               
               },
            credentials:"include"
         })
         const result = await res.json()
         if(result){
            console.log(`current user:`)
            console.log(result)
            setUser(result)
         }
      }
      getUser()
   },[])
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
      <div>
         <CartNav /> 
         <div className="grid grid-cols-12 gap-1 py-2 h-screen mt-22">       
            <div className="col-span-8 bg-amber-100">
               <p>Hello <span className="font-bold text-sky-400">{user?.username}</span>. Your cart: {cart?.totalItem} items</p>
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
                        </div>     */}
                        <div className="mt-auto">
                           <button 
                              onClick={()=>removeFromCart(pizzaItem)}
                              className="border border-blue-300 p-3 rounded cursor-pointer">Remove</button>
                        </div>                 
                     </div>
               </div>
               ))}
            
            </div>
            {/* <div className="col-span-4 bg-pink-100 border-left">
                <table>
                  <tr>
                     <th>Item</th><th>Qty</th><th>Sub Total</th>
                  </tr>
               {cartItems.map((pizzaItem)=>(
                  <div className="bg-green-100 border-bottom">                    
                     <tr>
                        <td>{pizzaItem.pizza.name}</td>
                        <td>{pizzaItem.quantity}</td>
                        <td>{pizzaItem.subAmount}</td>                      
                     </tr> 
                     <tr className="border border-dashed"></tr>                     
                  </div>                 
               ))}
               <p>Discount: ${cart.discount}</p>
               <p>Shipping Fee: ${cart.shippingFee}</p>
               <p>Taxes: ${cart.taxes}</p>
               <hr />
               <p>Total Items: {cart.totalItem}</p>
               <hr/>
               <p>Total Pay: ${cart.total}</p>
               
                 </table>
               <Link to="/user/pay" className="rounded-lg font-bold p-2 border">Pay with PayPal</Link>
            </div> */}
            <div className="col-span-4 bg-white border-l border-gray-200 rounded-lg shadow-lg p-6 m-2">
               <h2 className="text-xl font-bold mb-4 border-b pb-2">Your Cart</h2>
               <table className="w-full text-left border-collapse">
                  <thead className="bg-gray-100">
                     <tr>
                     <th className="p-2 text-sm font-medium">Item</th>
                     <th className="p-2 text-sm font-medium">Qty</th>
                     <th className="p-2 text-sm font-medium text-right">Sub Total</th>
                     </tr>
                  </thead>
                  <tbody>
                     {cartItems.map((pizzaItem, idx) => (
                     <tr key={idx} className="border-b hover:bg-gray-50 transition">
                        <td className="p-2">{pizzaItem.pizza.name}</td>
                        <td className="p-2">{pizzaItem.quantity}</td>
                        <td className="p-2 text-right">${pizzaItem.subAmount}</td>
                     </tr>
                     ))}
                  </tbody>
               </table>

               <div className="mt-4 space-y-1 text-sm">
                  <div className="flex justify-between">
                     <span>Discount:</span>
                     <span>${cart.discount}</span>
                  </div>
                  <div className="flex justify-between">
                     <span>Shipping Fee:</span>
                     <span>${cart.shippingFee}</span>
                  </div>
                  <div className="flex justify-between">
                     <span>Taxes:</span>
                     <span>${cart.taxes.toFixed(2)}</span>
                  </div>
               </div>

               <hr className="my-3 border-gray-300" />

               <div className="flex justify-between font-semibold text-lg">
                  <span>Total Items:</span>
                  <span>{cart.totalItem}</span>
               </div>

               <div className="flex justify-between font-bold text-xl mt-1 mb-4">
                  <span>Total Pay:</span>
                  <span>${cart.total.toFixed(2)}</span>
               </div>

               <Link
                  to="/user/pay"
                  className="block w-full text-center bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 rounded-lg transition"
               >
                  Pay with PayPal
               </Link>
            </div>

        </div>
      </div>
     
   )
}