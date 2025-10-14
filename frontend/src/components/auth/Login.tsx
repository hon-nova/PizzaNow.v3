import { useState } from 'react'
import { useNavigate } from "react-router-dom" 
import { FcGoogle } from "react-icons/fc"
import { LiaLinkedin } from "react-icons/lia"

type Msg = {
   error: string,
   success: string
}
export function Login() {
   const [email, setEmail] = useState('')
   const [password, setPassword] = useState('')
   const navigate = useNavigate()

   const [msg, setMsg] = useState<Msg>({error: '',success:''})
   
   const BASE_URL ="http://auth.pizzanow.local.com:4016"
   console.log("AUTH URL:",BASE_URL);

   const handleSubmit = (e: React.FormEvent) => {
      e.preventDefault()
      
      console.log('Email:', email)
      console.log('Password:', password)
      
      async function loginUser(){
         const res = await fetch(`${BASE_URL}/api/auth/login`,{
            method:"POST",
            headers:{
               "Content-Type":"application/json",               
            },
            body: JSON.stringify({email,password}),
            credentials: "include"
         })
      
         const result = await res.json()
         console.log(`IMPORTANT: result /login: `)
         console.log(result)

         if (result?.message!=="Login Success"){
            console.log(result.message)
            setMsg((pre:Msg)=>({...pre,error: result?.detail}))         
            setTimeout(()=>{
               setMsg((pre:Msg)=>({...pre,error: ""}))
            },4000)
            return; 
            }              
         
         setMsg((pre:Msg)=>({...pre, success:result?.message}))         
         setTimeout(()=>{
            navigate('/products')
         },2000)  
      }
      loginUser()
      setEmail("")
      setPassword("")
   }

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-200">
      <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-md">
        <h2 className="text-2xl font-bold text-amber-600 mb-6 text-center">Login</h2>
        <div className='h-[50px]'>
            {msg && msg?.error && (
            <div className="bg-red-100 text-red-700 p-2 rounded mb-4 text-center">{msg.error}</div>
         )}
            {msg && msg?.success && (
            <div className="bg-green-100 text-green-700 p-2 rounded mb-4 text-center">{msg.success}</div>
         )}
        </div>        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-neutral-700 mb-1">
              Email Address
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full px-4 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-amber-600"
              required
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-neutral-700 mb-1">
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-4 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-amber-600"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-amber-600 text-whitesmoke py-2 rounded font-semibold hover:bg-amber-500 transition-colors"
          >Sign In</button>
        </form>
        <p className="mt-4 text-center text-neutral-500 text-sm">
          Don't have an account? <a href="/register" className="text-amber-600 hover:underline">Sign Up</a>
        </p>
        <div className='border-b border-gray-300 border-b-6 py-3'>
         {/* Google + LinkedIn */}
         
         <p className='text-center text-gray-500 my-1'>Or</p>
         <hr className="text-gray-300 shadow-md w-[210px] mx-auto"/>        
          <div className="flex flex-col justify-center items-center mt-3">            
            <button
               onClick={() => {
                  window.location.href = `${import.meta.env.VITE_AUTH_BACKEND_URL}/api/auth/google/login`;
               }}
               className="flex flex-row space-x-2 bg-black text-white py-2 px-4 rounded-full border rounded cursor-pointer"
               > <FcGoogle size={30}/> <span>Sign in with Google</span>
            </button>
            <button
               onClick={() => {
                  window.location.href = `${import.meta.env.VITE_AUTH_BACKEND_URL}/api/auth/linkedin/login`
               }}
               className="flex flex-row justify-center space-x-2 bg-blue-700 text-white py-2 px-4 rounded-full border rounded cursor-pointer"
               > <LiaLinkedin size={30}/> <span>Sign in with LinkedIn</span>
               
            </button>
         </div>
        </div>
      </div>
    </div>
  )
}


