export const Footer = () => {
  return (
    <footer className="w-full bg-gray-300 border-t border-amber-600 mt-10 py-6 text-center text-sm text-gray-600">
      <p>🍕 PizzaNow &copy; {new Date().getFullYear()} — All rights reserved.</p>
      <p className="mt-2">
        Built with LangGraph, React, FastAPI, and a whole lot of cheese.
      </p>
    </footer>
  )
}