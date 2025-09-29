import { useState, useEffect } from "react"
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js"
import { useUserStore } from "../stores/userStore"
import { useCartStore } from "../stores/cartStore"

function Message({ content }:{content:string}) {
  if (!content) return null
  return <p className="mt-2 text-center text-sm text-gray-700">{content}</p>
}

export function PayPal() {
   const { user, setUser } = useUserStore()
   const userId = user?.id
   console.log(`paypal user: ${user}`)
   const { cart, setUserId } = useCartStore()
   const BASE_PAYPAL_URL = import.meta.env.VITE_PAYPAL_BACKEND_URL
   const cartItems = cart?.cartItems || []

   const [message, setMessage] = useState("")  

   const initialOptions = {
         clientId: import.meta.env.VITE_PAYPAL_CLIENT_ID,
         enableFunding: "venmo",
         buyerCountry: "CA",
         currency: "CAD",
         components: "buttons",
      }
   useEffect(()=>{
      async function getUser(){
         const res = await fetch(`${BASE_PAYPAL_URL}/api/paypal/auth`,{
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
      useEffect(()=>{
      if (userId){
         setUserId(userId)
      }
   },[setUserId,userId])

  return (
    <div className="grid grid-cols-12 gap-6 p-6 h-screen bg-gray-50">

      {/* LEFT COLUMN: Cart Details */}
      <div className="col-span-7 bg-white rounded-xl shadow-lg p-6 overflow-y-auto">
        <h2 className="text-2xl font-bold mb-4 border-b pb-2">Your Cart</h2>

        <table className="w-full border-collapse">
          <thead className="bg-gray-100 rounded-t-lg">
            <tr>
              <th className="p-3 text-sm font-medium text-left">Item</th>
              <th className="p-3 text-sm font-medium text-center">Qty</th>
              <th className="p-3 text-sm font-medium text-right">Sub Total</th>
            </tr>
          </thead>
          <tbody>
            {cartItems.map((pizzaItem, idx) => (
              <tr key={idx} className="border-b hover:bg-gray-50 transition-all">
                <td className="p-3">{pizzaItem.pizza.name}</td>
                <td className="p-3 text-center">{pizzaItem.quantity}</td>
                <td className="p-3 text-right">${pizzaItem.subAmount.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="mt-4 space-y-1 text-sm text-gray-600">
          <div className="flex justify-between">
            <span>Discount:</span>
            <span>${cart.discount?.toFixed(2) || 0}</span>
          </div>
          <div className="flex justify-between">
            <span>Shipping Fee:</span>
            <span>${cart.shippingFee?.toFixed(2) || 0}</span>
          </div>
          <div className="flex justify-between">
            <span>Taxes:</span>
            <span>${cart.taxes?.toFixed(2) || 0}</span>
          </div>
        </div>

        <hr className="my-3 border-gray-300" />

        <div className="flex justify-between font-semibold text-lg">
          <span>Total Items:</span>
          <span>{cart.totalItem}</span>
        </div>

        <div className="flex justify-between font-bold text-xl mt-1 mb-4 text-yellow-700">
          <span>Total Pay:</span>
          <span>${cart.total?.toFixed(2)}</span>
        </div>
      </div>

      {/* RIGHT COLUMN: PayPal Buttons */}
      <div className="col-span-5 flex flex-col">
        <div className="bg-white rounded-xl shadow-lg p-6 flex flex-col">
          <h2 className="text-xl font-bold mb-4">Checkout with PayPal</h2>

          <PayPalScriptProvider options={initialOptions}>
            <PayPalButtons
              style={{ shape: "rect", layout: "vertical", color: "gold", label: "paypal" }}
              createOrder={async () => {
                const res = await fetch(`${BASE_PAYPAL_URL}/api/paypal/orders`, {
                  method: "POST",
                  headers: { 
                     "Content-Type": "application/json" },
                  body: JSON.stringify({ amount: cart.total.toFixed(2) }),
                })
               //  const data = await res.json()
               //  console.log(`data sent to the BE expecting id, status: /api/paypal/orders data: ${data.id} ${data.status}`)

               //  return data.id
               const orderId = await res.text() // <-- BE returns plain string
               console.log(`PayPal orderID: ${orderId}`)
               return orderId.replace(/"/g, "")
              }}
              onApprove={async (data) => {
               console.log(`IMPORTANT original PAYPAL onApprove() data: ${data}`)
                const res = await fetch(
                  `${BASE_PAYPAL_URL}/api/paypal/orders/${data.orderID}/capture`,
                  { 
                     method: "POST", 
                     headers: { "Content-Type": "application/json" },
                     body: JSON.stringify({
                        user_id: user?.id,
                     cart_items: cart.cartItems.map(item => ({
                        pizza_id: item.pizza.id,
                        quantity: item.quantity,
                        subAmount: item.subAmount,
                     })),
                     discount: cart.discount,
                     shippingFee: cart.shippingFee,
                     taxes: cart.taxes,
                     total: cart.total

                     }) }
                )
                const captureData = await res.json()
               // BE returns  {"status": "success", "order_id": saved_order.id, "paypal_order_id": paypal_order_id}
                const transaction = captureData.purchase_units[0].payments.captures[0]
                setMessage(`Transaction ${transaction.status}: ${transaction.id}`)
                console.log("Capture result", captureData)
              }}
            />
          </PayPalScriptProvider>

          <Message content={message} />
        </div>
      </div>
    </div>
  )
}
