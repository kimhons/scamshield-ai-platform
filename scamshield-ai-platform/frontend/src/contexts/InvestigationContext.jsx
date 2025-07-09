import React, { createContext, useContext, useState, useCallback } from 'react'
import { db } from '../lib/supabase'
import { useAuth } from './AuthContext'

const InvestigationContext = createContext({})

export const useInvestigation = () => {
  const context = useContext(InvestigationContext)
  if (!context) {
    throw new Error('useInvestigation must be used within an InvestigationProvider')
  }
  return context
}

export const InvestigationProvider = ({ children }) => {
  const { user } = useAuth()
  const [investigations, setInvestigations] = useState([])
  const [currentInvestigation, setCurrentInvestigation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const createInvestigation = useCallback(async (investigationData) => {
    if (!user) return { data: null, error: 'User not authenticated' }
    
    try {
      setLoading(true)
      setError(null)
      
      const newInvestigation = {
        ...investigationData,
        user_id: user.id,
        status: 'pending',
        created_at: new Date().toISOString()
      }
      
      const { data, error } = await db.investigations.create(newInvestigation)
      
      if (error) throw error
      
      if (data) {
        setInvestigations(prev => [data[0], ...prev])
        setCurrentInvestigation(data[0])
      }
      
      return { data: data?.[0], error: null }
    } catch (err) {
      setError(err.message)
      return { data: null, error: err.message }
    } finally {
      setLoading(false)
    }
  }, [user])

  const loadInvestigations = useCallback(async () => {
    if (!user) return
    
    try {
      setLoading(true)
      setError(null)
      
      const { data, error } = await db.investigations.getByUserId(user.id)
      
      if (error) throw error
      
      setInvestigations(data || [])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [user])

  const loadInvestigation = useCallback(async (id) => {
    try {
      setLoading(true)
      setError(null)
      
      const { data, error } = await db.investigations.getById(id)
      
      if (error) throw error
      
      setCurrentInvestigation(data)
      return { data, error: null }
    } catch (err) {
      setError(err.message)
      return { data: null, error: err.message }
    } finally {
      setLoading(false)
    }
  }, [])

  const updateInvestigation = useCallback(async (id, updates) => {
    try {
      setLoading(true)
      setError(null)
      
      const { data, error } = await db.investigations.update(id, updates)
      
      if (error) throw error
      
      if (data) {
        setInvestigations(prev => 
          prev.map(inv => inv.id === id ? data[0] : inv)
        )
        if (currentInvestigation?.id === id) {
          setCurrentInvestigation(data[0])
        }
      }
      
      return { data: data?.[0], error: null }
    } catch (err) {
      setError(err.message)
      return { data: null, error: err.message }
    } finally {
      setLoading(false)
    }
  }, [currentInvestigation])

  const value = {
    investigations,
    currentInvestigation,
    loading,
    error,
    createInvestigation,
    loadInvestigations,
    loadInvestigation,
    updateInvestigation,
    setCurrentInvestigation
  }

  return (
    <InvestigationContext.Provider value={value}>
      {children}
    </InvestigationContext.Provider>
  )
}