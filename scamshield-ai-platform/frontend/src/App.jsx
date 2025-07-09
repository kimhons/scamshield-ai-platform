import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { InvestigationProvider } from './contexts/InvestigationContext'
import EnterpriseLandingPage from './components/enterprise/EnterpriseLandingPage'
import { EnterpriseLoginForm, EnterpriseSignupForm } from './components/enterprise/EnterpriseAuth'
import EnterpriseDashboard from './components/enterprise/EnterpriseDashboard'
import Investigations from './pages/Investigations'
import InvestigationDetails from './pages/InvestigationDetails'
import InvestigationForm from './components/investigations/InvestigationForm'
import EnterpriseLayout from './components/enterprise/EnterpriseLayout'
import './index.css'

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth()
  
  if (loading) {
    return (
      <EnterpriseLayout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-600">Loading...</p>
          </div>
        </div>
      </EnterpriseLayout>
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
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
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
                    <EnterpriseLayout>
                      <EnterpriseLandingPage />
                    </EnterpriseLayout>
                  </PublicRoute>
                } 
              />
              <Route 
                path="/login" 
                element={
                  <PublicRoute>
                    <EnterpriseLoginForm />
                  </PublicRoute>
                } 
              />
              <Route 
                path="/signup" 
                element={
                  <PublicRoute>
                    <EnterpriseSignupForm />
                  </PublicRoute>
                } 
              />
              
              {/* Protected Routes */}
              <Route 
                path="/dashboard" 
                element={
                  <ProtectedRoute>
                    <EnterpriseLayout>
                      <EnterpriseDashboard />
                    </EnterpriseLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/investigations" 
                element={
                  <ProtectedRoute>
                    <EnterpriseLayout>
                      <Investigations />
                    </EnterpriseLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/investigations/new" 
                element={
                  <ProtectedRoute>
                    <EnterpriseLayout>
                      <InvestigationForm />
                    </EnterpriseLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/investigations/:id" 
                element={
                  <ProtectedRoute>
                    <EnterpriseLayout>
                      <InvestigationDetails />
                    </EnterpriseLayout>
                  </ProtectedRoute>
                } 
              />
              
              {/* Placeholder routes for future enterprise features */}
              <Route 
                path="/reports" 
                element={
                  <ProtectedRoute>
                    <EnterpriseLayout>
                      <div className="container-enterprise py-16">
                        <div className="text-center">
                          <h1 className="text-3xl font-bold text-gray-900 mb-4">Enterprise Reports</h1>
                          <p className="text-gray-600 mb-6">Advanced reporting and analytics dashboard coming soon.</p>
                          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 max-w-md mx-auto">
                            <h3 className="text-lg font-semibold text-blue-900 mb-2">What's Coming</h3>
                            <ul className="text-sm text-blue-800 space-y-1 text-left">
                              <li>• Executive summary reports</li>
                              <li>• Compliance documentation</li>
                              <li>• Custom report builder</li>
                              <li>• Automated report scheduling</li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </EnterpriseLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/analytics" 
                element={
                  <ProtectedRoute>
                    <EnterpriseLayout>
                      <div className="container-enterprise py-16">
                        <div className="text-center">
                          <h1 className="text-3xl font-bold text-gray-900 mb-4">Security Analytics</h1>
                          <p className="text-gray-600 mb-6">Advanced security analytics and threat intelligence platform.</p>
                          <div className="bg-green-50 border border-green-200 rounded-lg p-6 max-w-md mx-auto">
                            <h3 className="text-lg font-semibold text-green-900 mb-2">Enterprise Features</h3>
                            <ul className="text-sm text-green-800 space-y-1 text-left">
                              <li>• Real-time threat monitoring</li>
                              <li>• Predictive fraud modeling</li>
                              <li>• Custom risk scoring</li>
                              <li>• Industry benchmarking</li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </EnterpriseLayout>
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/profile" 
                element={
                  <ProtectedRoute>
                    <EnterpriseLayout>
                      <div className="container-enterprise py-16">
                        <div className="text-center">
                          <h1 className="text-3xl font-bold text-gray-900 mb-4">Enterprise Settings</h1>
                          <p className="text-gray-600 mb-6">Manage your enterprise account settings and preferences.</p>
                          <div className="bg-purple-50 border border-purple-200 rounded-lg p-6 max-w-md mx-auto">
                            <h3 className="text-lg font-semibold text-purple-900 mb-2">Account Management</h3>
                            <ul className="text-sm text-purple-800 space-y-1 text-left">
                              <li>• User management & roles</li>
                              <li>• SSO configuration</li>
                              <li>• API key management</li>
                              <li>• Compliance settings</li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </EnterpriseLayout>
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