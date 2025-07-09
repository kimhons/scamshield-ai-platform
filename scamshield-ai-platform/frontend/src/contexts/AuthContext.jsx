import React, { createContext, useContext, useEffect, useState } from 'react'
import { auth } from '../lib/supabase'

const AuthContext = createContext({})

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)
  const [profile, setProfile] = useState(null)

  useEffect(() => {
    // Get initial session
    const getInitialSession = async () => {
      const { data: { session } } = await auth.getSession()
      setSession(session)
      setUser(session?.user ?? null)
      setLoading(false)
    }

    getInitialSession()

    // Listen for auth changes
    const { data: { subscription } } = auth.onAuthStateChange(
      async (event, session) => {
        setSession(session)
        setUser(session?.user ?? null)
        setLoading(false)
        
        // Clear profile when signing out
        if (event === 'SIGNED_OUT') {
          setProfile(null)
        }
      }
    )

    return () => subscription.unsubscribe()
  }, [])

  const signUp = async (email, password, userData = {}) => {
    try {
      setLoading(true)
      const { data, error } = await auth.signUp(email, password, {
        data: userData
      })
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      return { data: null, error }
    } finally {
      setLoading(false)
    }
  }

  const signIn = async (email, password) => {
    try {
      setLoading(true)
      
      // Demo authentication bypass for testing
      if (email === 'demo@nexussecurity.ai' && password === 'demo123') {
        const demoUser = {
          id: 'demo-user-id',
          email: 'demo@nexussecurity.ai',
          user_metadata: {
            name: 'Demo User',
            role: 'admin'
          }
        }
        const demoSession = {
          user: demoUser,
          access_token: 'demo-token',
          expires_at: Date.now() + 24 * 60 * 60 * 1000 // 24 hours
        }
        
        setUser(demoUser)
        setSession(demoSession)
        return { data: { session: demoSession }, error: null }
      }
      
      // Regular Supabase authentication
      const { data, error } = await auth.signIn(email, password)
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      // If Supabase is not configured, allow demo login
      if (email === 'demo@nexussecurity.ai' && password === 'demo123') {
        const demoUser = {
          id: 'demo-user-id',
          email: 'demo@nexussecurity.ai',
          user_metadata: {
            name: 'Demo User',
            role: 'admin'
          }
        }
        const demoSession = {
          user: demoUser,
          access_token: 'demo-token',
          expires_at: Date.now() + 24 * 60 * 60 * 1000
        }
        
        setUser(demoUser)
        setSession(demoSession)
        return { data: { session: demoSession }, error: null }
      }
      
      return { data: null, error }
    } finally {
      setLoading(false)
    }
  }

  const signOut = async () => {
    try {
      setLoading(true)
      const { error } = await auth.signOut()
      if (error) throw error
    } catch (error) {
      console.error('Error signing out:', error)
    } finally {
      setLoading(false)
    }
  }

  const value = {
    user,
    session,
    profile,
    loading,
    signUp,
    signIn,
    signOut
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}