import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { InvestigationProvider } from './contexts/InvestigationContext'
import ModernLandingPage from './components/ModernLandingPage'
import LoginForm from './components/auth/LoginForm'
import PremiumLoginForm from './components/auth/PremiumLoginForm'
import SignupForm from './components/auth/SignupForm'
import Dashboard from './pages/Dashboard'
import Investigations from './pages/Investigations'
import InvestigationDetails from './pages/InvestigationDetails'
import InvestigationForm from './components/investigations/InvestigationForm'
import Layout from './components/layout/Layout'
import PremiumLayout from './components/layout/PremiumLayout'
import PremiumDashboard from './components/dashboard/PremiumDashboard'
import './App.css'

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth()
  
  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-300">Loading...</p>
          </div>
        </div>
      </Layout>
    )
  }
  
  if (!user) {
    return <Navigate to="/login" replace />
  }
  
  return children
}

// Public Route Component (redirect if authenticated)
const PublicRoute = ({ children }) => {
  const { user, loading } = useAuth()
  
  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-300">Loading...</p>
          </div>
        </div>
      </Layout>
    )
  }
  
  if (user) {
    return <Navigate to="/dashboard" replace />
  }
  
  return children
}

function App() {
  return (
    <AuthProvider>
      <InvestigationProvider>
        <Router>
          <div className="App">
            <Routes>
              {/* Public Routes */}
              <Route 
                path="/" 
                element={
                  <PublicRoute>
                    <ModernLandingPage />
                  </PublicRoute>
                } 
              />
              <Route 
                path="/login" 
                element={
                  <PublicRoute>
                    <PremiumLoginForm />
                  </PublicRoute>
                } 
              />
              <Route 
                path="/signup" 
                element={
                  <PublicRoute>
                    <Layout>
                      <SignupForm />
                    </Layout>
                  </PublicRoute>
                } 
              />
              
              {/* Protected Routes */}
              <Route 
                path="/dashboard" 
                element={
                  <ProtectedRoute>
                    <PremiumLayout>
                      <PremiumDashboard />
                    </PremiumLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/investigations" 
                element={
                  <ProtectedRoute>
                    <PremiumLayout>
                      <Investigations />
                    </PremiumLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/investigations/new" 
                element={
                  <ProtectedRoute>
                    <PremiumLayout>
                      <InvestigationForm />
                    </PremiumLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/investigations/:id" 
                element={
                  <ProtectedRoute>
                    <PremiumLayout>
                      <InvestigationDetails />
                    </PremiumLayout>
                  </ProtectedRoute>
                } 
              />
              
              {/* Placeholder routes for future features */}
              <Route 
                path="/reports" 
                element={
                  <ProtectedRoute>
                    <PremiumLayout>
                      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                        <div className="text-center">
                          <h1 className="text-3xl font-bold gradient-text font-tech mb-4">Reports</h1>
                          <p className="text-muted-foreground">Advanced reporting features coming soon!</p>
                        </div>
                      </div>
                    </PremiumLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/analytics" 
                element={
                  <ProtectedRoute>
                    <PremiumLayout>
                      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                        <div className="text-center">
                          <h1 className="text-3xl font-bold gradient-text-blue font-tech mb-4">Analytics</h1>
                          <p className="text-muted-foreground">Deep analytics and insights coming soon!</p>
                        </div>
                      </div>
                    </PremiumLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/settings" 
                element={
                  <ProtectedRoute>
                    <PremiumLayout>
                      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                        <div className="text-center">
                          <h1 className="text-3xl font-bold gradient-text font-tech mb-4">Settings</h1>
                          <p className="text-muted-foreground">Configuration and preferences coming soon!</p>
                        </div>
                      </div>
                    </PremiumLayout>
                  </ProtectedRoute>
                } 
              />
              
              {/* Fallback route */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </div>
        </Router>
      </InvestigationProvider>
    </AuthProvider>
  )
}

export default App