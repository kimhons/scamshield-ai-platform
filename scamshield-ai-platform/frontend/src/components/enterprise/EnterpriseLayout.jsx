import React from 'react'
import EnterpriseHeader from './EnterpriseHeader'

const EnterpriseLayout = ({ children, className = '' }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <EnterpriseHeader />
      
      <main className={`${className}`}>
        {children}
      </main>
    </div>
  )
}

export default EnterpriseLayout