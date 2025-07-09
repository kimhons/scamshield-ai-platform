import React, { useState } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { useNavigate, useLocation } from 'react-router-dom'
import { Button } from '../ui/button'
import {
  Shield, Menu, X, User, LogOut, Settings, Bell,
  Search, Zap, Crown, ChevronDown
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const Header = () => {
  const { user, signOut } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [profileMenuOpen, setProfileMenuOpen] = useState(false)

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: Shield },
    { name: 'Investigations', href: '/investigations', icon: Search },
    { name: 'Reports', href: '/reports', icon: Crown },
    { name: 'Analytics', href: '/analytics', icon: Zap },
  ]

  const handleSignOut = async () => {
    await signOut()
    navigate('/')
  }

  return (
    <header className="sticky top-0 z-50 bg-black/20 backdrop-blur-xl border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate('/')}>
            <div className="relative">
              <Shield className="h-8 w-8 text-orange-500" />
              <div className="absolute inset-0 h-8 w-8 text-orange-500 animate-pulse opacity-50"></div>
            </div>
            <div>
              <span className="text-xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                ScamShield
              </span>
              <span className="text-xl font-bold bg-gradient-to-r from-orange-500 to-yellow-500 bg-clip-text text-transparent ml-1">
                AI
              </span>
            </div>
          </div>

          {/* Desktop Navigation */}
          {user && (
            <nav className="hidden md:flex space-x-8">
              {navigation.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.href
                return (
                  <button
                    key={item.name}
                    onClick={() => navigate(item.href)}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-200 ${
                      isActive
                        ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30'
                        : 'text-gray-300 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{item.name}</span>
                  </button>
                )
              })}
            </nav>
          )}

          {/* Right side */}
          <div className="flex items-center space-x-4">
            {user ? (
              <>
                {/* Notifications */}
                <button className="relative p-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                  <Bell className="w-5 h-5" />
                  <span className="absolute top-1 right-1 w-2 h-2 bg-orange-500 rounded-full"></span>
                </button>

                {/* Profile Menu */}
                <div className="relative">
                  <button
                    onClick={() => setProfileMenuOpen(!profileMenuOpen)}
                    className="flex items-center space-x-2 p-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                  >
                    <div className="w-8 h-8 bg-gradient-to-r from-orange-500 to-red-500 rounded-full flex items-center justify-center">
                      <User className="w-4 h-4 text-white" />
                    </div>
                    <ChevronDown className="w-4 h-4" />
                  </button>

                  {/* Profile Dropdown */}
                  <AnimatePresence>
                    {profileMenuOpen && (
                      <motion.div
                        initial={{ opacity: 0, scale: 0.95, y: -10 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95, y: -10 }}
                        className="absolute right-0 mt-2 w-48 bg-black/80 backdrop-blur-xl border border-white/10 rounded-xl shadow-2xl"
                      >
                        <div className="py-2">
                          <div className="px-4 py-2 border-b border-white/10">
                            <p className="text-sm text-gray-300">{user.email}</p>
                          </div>
                          <button
                            onClick={() => {
                              navigate('/profile')
                              setProfileMenuOpen(false)
                            }}
                            className="flex items-center space-x-2 w-full px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 transition-colors"
                          >
                            <Settings className="w-4 h-4" />
                            <span>Settings</span>
                          </button>
                          <button
                            onClick={handleSignOut}
                            className="flex items-center space-x-2 w-full px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 transition-colors"
                          >
                            <LogOut className="w-4 h-4" />
                            <span>Sign Out</span>
                          </button>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </>
            ) : (
              <div className="flex items-center space-x-4">
                <Button
                  variant="ghost"
                  onClick={() => navigate('/login')}
                  className="text-gray-300 hover:text-white"
                >
                  Sign In
                </Button>
                <Button
                  variant="gradient"
                  onClick={() => navigate('/signup')}
                  className="transform hover:scale-105"
                >
                  Get Started
                </Button>
              </div>
            )}

            {/* Mobile menu button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-black/40 backdrop-blur-xl border-t border-white/10"
          >
            <div className="px-4 py-4 space-y-2">
              {user && navigation.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.href
                return (
                  <button
                    key={item.name}
                    onClick={() => {
                      navigate(item.href)
                      setMobileMenuOpen(false)
                    }}
                    className={`flex items-center space-x-3 w-full px-4 py-3 rounded-lg transition-colors ${
                      isActive
                        ? 'bg-orange-500/20 text-orange-400'
                        : 'text-gray-300 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{item.name}</span>
                  </button>
                )
              })}
              
              {!user && (
                <div className="pt-4 space-y-3">
                  <Button
                    variant="outline"
                    onClick={() => {
                      navigate('/login')
                      setMobileMenuOpen(false)
                    }}
                    className="w-full"
                  >
                    Sign In
                  </Button>
                  <Button
                    variant="gradient"
                    onClick={() => {
                      navigate('/signup')
                      setMobileMenuOpen(false)
                    }}
                    className="w-full"
                  >
                    Get Started
                  </Button>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  )
}

export default Header