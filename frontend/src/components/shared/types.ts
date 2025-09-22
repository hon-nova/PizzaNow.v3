export type User = {
   id: string
   username: string 
   email:string
   password:string
   avatar:string
   role:string
   createdAt:string
   provider:string
   providerId?:string
}

export type Pizza  = {
   id: string           
   name: string
   description: string | null
   full_price: number   
   slice_price: number   
   image_url: string
   ingredients: string[]
}
export type Item = {
   pizza: Pizza
   quantity:number
   unit_type:string
   subAmount: number
}
export type Cart = {
   userId: string
   cartItems: Item[]
   subTotal:number
   taxes: number
   shippingFee: number,
   discount: number
   total:number
   totalItem: number
}