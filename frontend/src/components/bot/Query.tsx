// import { useState, useRef, useEffect } from "react"
// import axios from "axios"
// import styles from "./style/query.module.css"
// import { Link, useNavigate } from "react-router-dom"

// interface Message {
//   sender: "user" | "bot"
//   text: string
// }

// export function Query() {
//    // const [messages, setMessages] = useState<Message[]>([])
//    // const [input, setInput] = useState("")
//    // const [user, setUser] = useState({username:'',email:'',avatar:''})
//    // console.log("user from auth_route: ")
//    // console.log(user)
   
//    // const navigate = useNavigate()
//    // const BASE_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000"
   
//    // console.log(`Initial BASE_URL: ${BASE_URL}`)
//    // async function getUser(){
//    //    const res = await fetch(`${BASE_URL}/api/auth/me`,{
//    //       method:"GET",
//    //       headers:{
//    //             "Content-Type":"application/json",               
//    //          },
//    //       credentials:"include"
//    //    })
//    //    const result = await res.json()
//    //    if(result){
//    //       console.log(`current user:`)
//    //       console.log(result)
//    //       setUser(result)
//    //    }
//    // }
//    // useEffect(()=>{
//    //    getUser()
//    // },[])

//    // useEffect(()=>{
//    //    const verifyToken = async () => {
//    //       const res = await fetch(`${BASE_URL}/api/auth/verify-token`, {
//    //          method: "GET",
//    //          headers: {
//    //             "Content-Type": "application/json"
//    //          },
//    //          credentials: "include"
//    //       })
//    //       const result = await res.json()
//    //       console.log(`IMPORTANT result: ${result}`)
//    //       if (result?.detail){
//    //          console.log(`Token verification failed: ${result.detail}`)
//    //          navigate("/")
//    //       }
//    //       if (result) {
//    //          console.log(`Token verification result:`)
//    //          console.log(result)
//    //          //  navigate("/query")
//    //       }
//    //    }
//    //    verifyToken()
//    // },[])
//    // const inputRef = useRef<HTMLInputElement>(null)
//    // useEffect(() => {
//    //    if (inputRef.current) {
//    //       inputRef.current.focus();
//    //       }
//    //    }, [])
//    const sendMessage = async () => {
//        if (!input) return      
//       const userMessage: Message = { sender: "user", text: input }
//       setMessages((prev) => [...prev, userMessage])
//       setInput("")
//       if (inputRef.current) {
//          inputRef.current.focus(); // re-focus after send
//       }
//       try {
//          const res = await axios.post(`${BASE_URL}/query`, 
//             { text: input },
//             {withCredentials: true,
//                headers: {
//                   'Content-Type': 'application/json'
//                }}
//             )
//          console.log(`IMPORTANT Response from backend: ${JSON.stringify(res.data)}`)
//          const botMessage: Message = { sender: "bot", text: res.data.response }
//          setMessages((prev) => [...prev, botMessage])
//       } catch(err){
//          console.error(err)
//          setMessages((prev) => [...prev, { sender: "bot", text: "Something went wrong! Probably you are not logged in." }])
//       }
      
//   }
//   const messagesEndRef = useRef<HTMLDivElement | null>(null);

//    useEffect(() => {
//          messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
//    }, [messages]);
//    return (
//       <div className={`grid grid-cols-12`}>
//          <div className={`col-span-3 p-4 text-white ${styles.appSidebar}`}>           
            
//             {user?.username ? 
//             <div className="flex flex-row space-x-3 items-center">
//                <img src={user?.avatar} alt="avatar" className="rounded-full"/>
//                <p>{user.username}</p>
//             </div> : <Link className="cursor-pointer hover:underline" to="/">Login</Link>}
//          </div>
//           <div className={`col-span-9 h-screen flex items-center justify-center ${styles.appMain} p-4`}>
           
//          {user && <div className={`w-full max-w-2xl shadow-md rounded-lg flex flex-col overflow-y-auto h-150`}>               
//             <div className="flex-1 p-4 overflow-y-auto">
//                {messages.map((msg, idx) => (
//                   <div
//                      key={idx}
//                      className={`my-1 p-1 rounded-2xl max-w-[75%] ${
//                      msg.sender === "user"
//                         ? "bg-neutral-100 ml-auto text-left"
//                         : "bg-neutral-100 mr-auto text-left"
//                      }`}
//                   >
//                      {msg.sender === "user" ? (
//                      <p className={`mx-1 ${styles.msgUser}`}>{msg.text}</p>
//                      ) : (
//                      <p className={`mx-1 ${styles.msgAssistant}`}>{msg.text}</p>
//                      )}
//                   </div>
//                ))}
//                <div ref={messagesEndRef} />
//             </div>         
//             <div className="flex border-t p-2">               
//                <input
//                   className={`flex-1 border rounded p-2 text-white ${styles.queryMessage}`}
//                   placeholder="Ask anything"
//                   value={input}
//                   onChange={(e) => setInput(e.target.value)}
//                   onKeyDown={(e) => e.key === "Enter" && sendMessage()}  />               
//                <button className="ml-2 bg-blue-800 text-white rounded p-2" onClick={sendMessage}>
//                   Send
//                </button>
//             </div>
//          </div>}
//       </div>
//       </div>
     
//   )
// }