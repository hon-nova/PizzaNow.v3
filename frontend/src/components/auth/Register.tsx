import { useState } from "react"
import { useNavigate } from "react-router-dom" 

interface RegisterFormData {
  username: string
  email: string
  password: string
  confirm_password: string
}

type Msg = {
   error: string,
   success: string
}
export function Register() {
   const [formData, setFormData] = useState<RegisterFormData>({
      username: "",
      email: "",
      password: "",
      confirm_password: "",
   })
   const navigate = useNavigate()

  const [msg, setMsg] = useState<Msg>({error: '',success:''})

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setFormData({ ...formData, [e.target.name]: e.target.value })
      setMsg({
         error:'',
         success:''
      }) 
   }
   // VITE_AUTH_BACKEND_URL
   const BASE_URL = import.meta.env.VITE_AUTH_BACKEND_URL
   console.log(`BASE_URL: ${BASE_URL}`)

   const handleSubmit = (e: React.FormEvent) => {
      e.preventDefault()

      // if (formData.password !== formData.confirm_password) {         
      //    setMsg((pre:Msg)=>({ ...pre, error: "Passwords don't match!" }))  
        
      //    setTimeout(()=>{
      //       setMsg((pre:Msg)=>({...pre,error:""}))
      //    },2000)   
      //    return    
      // }
      async function addUser(){
         const res = await fetch(`${BASE_URL}/api/auth/register`,{
            method:"POST",
            headers :{
               "Content-Type":"application/json"
            },
            body: JSON.stringify(formData)
         })
         const result = await res.json()
         console.log(`IMPORTANT: result: `)
         console.log(result)
        
         if (!res.ok){
            console.log(`result`, result)            
         } 

         if (result?.detail){
            console.log(result.detail)
            setMsg((pre:Msg)=>({...pre,error: result.detail}))         
            setTimeout(()=>{
               setMsg((pre:Msg)=>({...pre,error: ""}))
            },4000)
            return; 
            }             
              
         if(result?.message){
            setMsg((pre:Msg)=>({...pre, success:result?.message}))         
            setTimeout(()=>{
               navigate('/')
            },4000)      
         }           
      }
      addUser()
      setFormData({
         username: "",
         email: "",
         password: "",
         confirm_password: "",
      })

   console.log("Registering user:", formData)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-200 p-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-amber-600 mb-6 text-center">Register</h2>
          <div className='h-[50px]'>
            {msg && msg.error && (
            <div className="bg-red-100 text-red-700 p-2 rounded mb-4 text-center">{msg.error}</div>
            )}
            {msg && msg.success && (
               <div className="bg-green-100 text-green-700 p-2 rounded mb-4 text-center">{msg.success}</div>
            )}
          </div>
       
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-1 text-neutral-700">Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className="w-full p-2 border border-neutral-300 rounded focus:outline-none focus:ring-2 focus:ring-amber-600"
              required
            />
          </div>
          <div>
            <label className="block mb-1 text-neutral-700">Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full p-2 border border-neutral-300 rounded focus:outline-none focus:ring-2 focus:ring-amber-600"
              required
            />
          </div>
          <div>
            <label className="block mb-1 text-neutral-700">Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="w-full p-2 border border-neutral-300 rounded focus:outline-none focus:ring-2 focus:ring-amber-600"
              required
            />
          </div>
          <div>
            <label className="block mb-1 text-neutral-700">Confirm Password</label>
            <input
              type="password"
              name="confirm_password"
              value={formData.confirm_password}
              onChange={handleChange}
              className="w-full p-2 border border-neutral-300 rounded focus:outline-none focus:ring-2 focus:ring-amber-600"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-amber-600 text-whitesmoke py-2 rounded font-semibold hover:bg-amber-500 transition-colors"
          >
            Register
          </button>
        </form>
        <p className="mt-4 text-center text-neutral-500 text-sm">
          Already have an account? <a href="/" className="text-amber-600 hover:underline">Login</a>
        </p>
      </div>
    </div>
  )
}


