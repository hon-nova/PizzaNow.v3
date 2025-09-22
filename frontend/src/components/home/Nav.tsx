// import styles from './Styles/home.module.css'
import { Link } from 'react-router-dom'
import { useEffect } from 'react'
import { useUserStore } from "../stores/userStore"
import { useCartStore } from '../stores/cartStore'
import { useNavigate } from 'react-router-dom'


export function Nav(){
   
   const navigate = useNavigate()  
   
   const { user,logout } = useUserStore();
   const userId = user?.id;
   const { cart, setUserId, setCart } = useCartStore();

   useEffect(() => {
      if (!userId) return
      setUserId(userId)      
   }, [userId,setCart,setUserId]);
   
   console.log(`@HomeNav (injection userId) userId from cart-storage: ${userId}`)
   const cart_length= cart?.totalItem
   console.log(`length cart: ${cart?.cartItems}`)

   function onLogout(){
      logout()
      navigate("/")
   }

   return (
     <nav className='border-b-8 border-green-800'>
      <ul className={`fixed top-0 bg-amber-600 p-6 text-gray-800 text-xl w-full `}>        
         <div className="flex justify-between">
            <div className="cursor-pointer hover:bg-neutral-100 hover:text-black hover:rounded">
               {/* <Link to="/">
                  <div className='flex flex-row justify-center items-center'>
                     <img src="/assets/logo.jpg" alt="logo" width={100} height={100} className="rounded-full"/>
                  </div>               
               </Link> */}
            </div>
            <div className="flex flex-row justify-center items-center">
                {/* <div className="cursor-pointer hover:bg-neutral-200 hover:text-black hover:rounded p-2"><Link to="/api/pizzas"> Pizza Store</Link></div> */}
                {/* <div className="cursor-pointer hover:bg-neutral-200 hover:text-black hover:rounded p-2"><Link to="/api/benbot/chat"> <GiMegabot size={33}/></Link></div> */}
                 <div className="cursor-pointer hover:bg-neutral-200 hover:text-black hover:rounded p-2"><Link to="/user/cart">Cart ({cart_length})</Link></div>
                {user?.username ? 
               <div className="cursor-pointer hover:bg-neutral-200 hover:text-black hover:rounded p-2"><button onClick={onLogout}>Logout</button></div> :  
               <div className="cursor-pointer hover:bg-neutral-200 hover:text-black hover:rounded p-2"><Link to="/api/auth/login">Login</Link></div>}              
            </div>           
         </div>        
      </ul>
     </nav>
   )
}