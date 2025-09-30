import { useState,useEffect,useRef } from "react"
import { useNavigate } from "react-router-dom"
import axios from "axios"
import styles from "./style/query.module.css"
import { useUserStore } from "../stores/userStore"


interface Message {
   sender: "user" | "bot"
   text: string
}

export const BenBotChat = () => {
   const [open, setOpen] = useState(false)
   const [isIconOpen,setIsIconOpen] = useState(true)

   const [messages, setMessages] = useState<Message[]>([])
   const [input, setInput] = useState("")
   const navigate = useNavigate()

      const { user, setUser  } = useUserStore()
      console.log(`logged-in user: `, user )
     
      const BASE_URL = import.meta.env.VITE_BOT_BACKEND_URL
      
      console.log(`Initial BASE_URL: ${BASE_URL}`)   
      useEffect(()=>{
         async function getUser(){
            const res = await fetch(`${BASE_URL}/api/pizzas/auth`,{
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
   function handleOpenStatus(){
      setOpen(!open)
      setIsIconOpen(!isIconOpen)
   }
   
   // useEffect(()=>{
   //    const verifyToken = async () => {
   //       const res = await fetch(`${BASE_URL}/api/auth/verify-token`, {
   //          method: "GET",
   //          headers: {
   //             "Content-Type": "application/json"
   //          },
   //          credentials: "include"
   //       })
   //       const result = await res.json()
   //       console.log(`IMPORTANT result: ${result}`)
   //       if (result?.detail){
   //          console.log(`Token verification failed: ${result.detail}`)
   //          navigate("/")
   //       }
   //       if (result) {
   //          console.log(`Token verification result:`)
   //          console.log(result)
   //          //  navigate("/query")
   //       }
   //    }
   //    verifyToken()
   // },[])

   const inputRef = useRef<HTMLInputElement>(null)
   useEffect(() => {
      if (inputRef.current) {
         inputRef.current.focus();
         }
      }, [])
   
   const sendMessage = async(e:React.FormEvent<HTMLFormElement>) => {
      e.preventDefault()
       if (!input) return      
      const userMessage: Message = { sender: "user", text: input }
      setMessages((prev) => [...prev, userMessage])
      setInput("")
      if (inputRef.current) {
         inputRef.current.focus(); // re-focus after send
      }
      try {
         const res = await axios.post(`${BASE_URL}/api/query`, 
            { text: input },
            {withCredentials: true,
               headers: {
                  'Content-Type': 'application/json'
               }}
            )
         console.log(`IMPORTANT Response from backend: ${JSON.stringify(res.data)}`)
         const botMessage: Message = { sender: "bot", text: res.data.response }
         setMessages((prev) => [...prev, botMessage])
      } catch(err){
         console.error(err)
         setMessages((prev) => [...prev, { sender: "bot", text: "Something went wrong! Probably you are not logged in." }])
      }
      
   }
   const messagesEndRef = useRef<HTMLDivElement | null>(null)
  
   useEffect(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
}, [messages])

  return (
    <>
      {/* Floating button */}
      {isIconOpen && 
       <button
        onClick={handleOpenStatus}
        className="fixed bottom-4 right-4 bg-amber-600 text-white rounded-full w-12 h-12 flex items-center justify-center shadow-lg hover:bg-yellow-600"
      >
        🤖
      </button>}    

      {/* Chat window */}
      {open && (
        <div className="fixed bottom-3 right-4 w-115 h-130 bg-white border rounded-lg shadow-lg flex flex-col overflow-y-auto">
          {/* Header */}
          <div className="bg-sky-400 text-white p-2 flex justify-between items-center">
            <span>BenBot</span>
            <button onClick={handleOpenStatus}>✕</button>
          </div>
          {/* Messages area */}
          <div className="flex-1 p-2 overflow-y-auto">
            {/* <p>Hi! Need a pizza recommendation?</p> */}
            {messages.map((msg, idx) => (
               <div
                  key={idx}
                  className={`my-1 p-1 rounded-2xl max-w-[75%] ${
                  msg.sender === "user"
                     ? "bg-neutral-100 ml-auto text-left"
                     : "bg-neutral-100 mr-auto text-left"
                  }`} >
                  {msg.sender === "user" ? (
                  <p className={`mx-1 ${styles.msgUser}`}>{msg.text}</p>
                  ) : (
                  <p className={`mx-1 ${styles.msgAssistant}`}>{msg.text}</p>
                  )}
               </div>
               ))}
               <div ref={messagesEndRef} />
          </div>

          {/* Input area */}
          <div className="p-2 border-t border-4 border-neutral-300">
            <form action="" onSubmit={(e)=>sendMessage(e)}>
               <input
                  type="text"
                  value={input}
                  onChange={(e)=>setInput(e.target.value)}
                  onKeyDown={(e)=>e.key ==="Enter" && sendMessage}
                  placeholder="Type a message..."
                  className="w-full border border-neutral-300 shadow:md rounded-lg px-2 py-2" />
            </form>           
          </div>
        </div>
      )}
    </>
  )
}


