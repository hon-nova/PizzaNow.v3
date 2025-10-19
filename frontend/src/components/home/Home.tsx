import { Footer } from "./Footer"
import { Nav } from "../home/Nav"
import { useUserStore } from "../stores/userStore"
import { useCartStore } from "../stores/cartStore"
import { useEffect } from "react"
import { PizzaStore } from "../pizza/PizzaStore"
import { BenBotChat } from "../bot/BenBotChat"
import { useSearchParams } from "react-router-dom"
import { useState } from "react"

export function Home(){
   const { user, setUser  } = useUserStore()
   const { clearCart } = useCartStore()
   console.log(`clearCart: ${clearCart}`)
   console.log(`logged-in user: `, user )
   const [searchParams] = useSearchParams()
   const [showModel, setShowModel ] = useState(true)
        
   const success = searchParams.get("success");
   const BASE_URL = import.meta.env.VITE_AUTH_BACKEND_URL
   
   console.log(`success: ${success}`) 
   useEffect(()=>{
      async function getUser(){
         const res = await fetch(`${BASE_URL}/api/auth/me`,{
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

   return (
      <div className="flex flex-col min-h-screen">        
         {/* Nav */}
         <div className="my-1"><Nav /></div>        
         {/* main */}
         <div className="pt-20 border border-2 border-indigo-600">
         {user ? <div>Hi <span className="font-bold text-sky-400">{user.username}</span> </div>: "Welcome to PizzaNow!"}
         
          {success  &&  <div className="fixed inset-30 w-[500px] text-center h-[60px] mx-auto">
             {showModel &&  <div className="relative">              
               <div 
                  className="absolute top-0 right-1 text-green-800 font-bold cursor-pointer"
                  onClick={()=>setShowModel(false)}
                     >X
               </div>

               {/* success */}
                <div className="border border-green-600 border-[0.5px] text-green-600 p-4">Payment successful! 🎉</div>
            </div>        }
                   
          </div>}
         
            <PizzaStore />
            <BenBotChat/>            
         </div>
          {/* footer */}
         <div className="mt-auto">
            <Footer />
         </div>
      </div>
   )
}
// text-amber-600
// bg-gray-100