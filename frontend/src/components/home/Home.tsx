import { Footer } from "./Footer"
import { Nav } from "./Nav"
import { useUserStore } from "../stores/userStore"
import { useEffect } from "react"


import { PizzaStore } from "../pizza/PizzaStore"
import { BenBotChat } from "../bot/BenBotChat"


export function Home(){
   const { user, setUser  } = useUserStore()
   console.log(`logged-in user: `, user )
  
   const BASE_URL = import.meta.env.VITE_PROFILE_BACKEND_URL
   
   console.log(`Initial BASE_URL: ${BASE_URL}`)   
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