
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { Login } from "./components/auth/Login"
import { Register } from "./components/auth/Register"
// import { Query } from "./components/bot/Query"
import { Policy } from "./components/home/Policy"
import { Home } from "./components/home/Home"
import { PayPal } from "./components/paypal/PayPal"
import { Cart } from "./components/cart/Cart"

export default function App() {

   return(
      <Router>
         <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/register" element={<Register />} />           
            <Route path="/products" element={<Home />} />
            <Route path="/api/privacy-policy" element={<Policy />} />           
            <Route path="/user/cart" element={<Cart />} />           
            <Route path="/user/pay" element={<PayPal />} />           
           
         </Routes>
      </Router>
   )
}

