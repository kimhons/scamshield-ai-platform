import React from 'react'
import Header from './Header'
import { motion } from 'framer-motion'

const Layout = ({ children, className = '' }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiM5QzkyQUMiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMSIvPjwvZz48L2c+PC9zdmc+')] opacity-20"></div>
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-blue-600/10 via-purple-600/10 to-pink-600/10 animate-pulse"></div>
        
        {/* Floating particles */}
        <div className="absolute top-20 left-10 w-2 h-2 bg-orange-500 rounded-full animate-bounce opacity-60"></div>
        <div className="absolute top-40 right-20 w-3 h-3 bg-blue-500 rounded-full animate-pulse opacity-40"></div>
        <div className="absolute bottom-40 left-20 w-2 h-2 bg-purple-500 rounded-full animate-bounce opacity-50"></div>
        <div className="absolute bottom-20 right-10 w-3 h-3 bg-pink-500 rounded-full animate-pulse opacity-60"></div>
      </div>

      <Header />
      
      <motion.main
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className={`relative z-10 ${className}`}
      >
        {children}
      </motion.main>
    </div>
  )
}

export default Layout