import React from 'react'
import NexusHeader from './NexusHeader'
import NexusFooter from './NexusFooter'

const NexusLayout = ({ children, className = '', showFooter = true }) => {
  return (
    <div className="min-h-screen bg-white flex flex-col">
      <NexusHeader />
      <main className={`flex-1 pt-16 ${className}`}>
        {children}
      </main>
      {showFooter && <NexusFooter />}
    </div>
  )
}

export default NexusLayout
