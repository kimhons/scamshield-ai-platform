import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { InvestigationProvider } from './contexts/InvestigationContext'
import NexusLandingPage from './components/nexus/NexusLandingPage'
import { NexusLoginForm, NexusSignupForm } from './components/nexus/NexusAuth'
import NexusDashboard from './components/nexus/NexusDashboard'
import Investigations from './pages/Investigations'
import InvestigationDetails from './pages/InvestigationDetails'
import InvestigationForm from './components/investigations/InvestigationForm'
import NexusLayout from './components/nexus/NexusLayout'
import './index.css'

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth()
  
  if (loading) {
    return (
      <NexusLayout showFooter={false}>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-600">Loading...</p>
          </div>
        </div>
      </NexusLayout>
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
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
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
                    <NexusLayout>
                      <NexusLandingPage />
                    </NexusLayout>
                  </PublicRoute>
                } 
              />
              <Route 
                path="/login" 
                element={
                  <PublicRoute>
                    <NexusLoginForm />
                  </PublicRoute>
                } 
              />
              <Route 
                path="/signup" 
                element={
                  <PublicRoute>
                    <NexusSignupForm />
                  </PublicRoute>
                } 
              />
              
              {/* Protected Routes */}
              <Route 
                path="/dashboard" 
                element={
                  <ProtectedRoute>
                    <NexusLayout>
                      <NexusDashboard />
                    </NexusLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/investigations" 
                element={
                  <ProtectedRoute>
                    <NexusLayout>
                      <Investigations />
                    </NexusLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/investigations/new" 
                element={
                  <ProtectedRoute>
                    <NexusLayout>
                      <InvestigationForm />
                    </NexusLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/investigations/:id" 
                element={
                  <ProtectedRoute>
                    <NexusLayout>
                      <InvestigationDetails />
                    </NexusLayout>
                  </ProtectedRoute>
                } 
              />
              
              {/* Placeholder routes for future features */}
              <Route 
                path="/reports" 
                element={
                  <ProtectedRoute>
                    <NexusLayout>
                      <div className="container-nexus section-nexus">
                        <div className="text-center">
                          <h1 className="nexus-heading-2 mb-4">Intelligence Reports</h1>
                          <p className="nexus-body-large text-gray-600 mb-6">Advanced reporting and analytics dashboard coming soon.</p>
                          <div className="card-nexus p-8 max-w-md mx-auto">
                            <h3 className="text-lg font-semibold text-blue-900 mb-4">What's Coming</h3>
                            <ul className="text-sm text-blue-800 space-y-2 text-left">
                              <li>• Executive summary reports</li>
                              <li>• Threat intelligence briefings</li>
                              <li>• Custom report builder</li>
                              <li>• Automated report scheduling</li>
                              <li>• Compliance documentation</li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </NexusLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/analytics" 
                element={
                  <ProtectedRoute>
                    <NexusLayout>
                      <div className="container-nexus section-nexus">
                        <div className="text-center">
                          <h1 className="nexus-heading-2 mb-4">Security Analytics</h1>
                          <p className="nexus-body-large text-gray-600 mb-6">Advanced security analytics and threat intelligence platform.</p>
                          <div className="card-nexus p-8 max-w-md mx-auto">
                            <h3 className="text-lg font-semibold text-green-900 mb-4">AI-Powered Features</h3>
                            <ul className="text-sm text-green-800 space-y-2 text-left">
                              <li>• Real-time threat monitoring</li>
                              <li>• Predictive threat modeling</li>
                              <li>• Custom risk scoring</li>
                              <li>• Industry benchmarking</li>
                              <li>• Behavioral analytics</li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </NexusLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/profile" 
                element={
                  <ProtectedRoute>
                    <NexusLayout>
                      <div className="container-nexus section-nexus">
                        <div className="text-center">
                          <h1 className="nexus-heading-2 mb-4">Account Settings</h1>
                          <p className="nexus-body-large text-gray-600 mb-6">Manage your Nexus Guard account settings and preferences.</p>
                          <div className="card-nexus p-8 max-w-md mx-auto">
                            <h3 className="text-lg font-semibold text-purple-900 mb-4">Account Management</h3>
                            <ul className="text-sm text-purple-800 space-y-2 text-left">
                              <li>• Profile and preferences</li>
                              <li>• Security settings</li>
                              <li>• API key management</li>
                              <li>• Notification preferences</li>
                              <li>• Team management</li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </NexusLayout>
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
