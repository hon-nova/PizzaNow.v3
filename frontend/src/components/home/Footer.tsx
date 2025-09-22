export function Footer(){

   return(
      <footer className={`w-full bg-amber-600 text-center p-5 text-gray-800 text-xl`}>
         Developed and maintained by Hon Nguyen
         <div className="w-full text-center text-gray-300 text-sm py-4">
            © {new Date().getFullYear()} PizzaNow | <a href="/api/privacy-policy" className="underline hover:text-gray-200">Privacy Policy</a>
         </div>
      </footer>
   )
}