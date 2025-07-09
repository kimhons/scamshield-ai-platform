import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://unnrwgigpoewjuahspip.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVubnJ3Z2lncG9ld2p1YWhzcGlwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwMzcyMDksImV4cCI6MjA2NzYxMzIwOX0.I1A7gZPse01XUcr-snPWWn-mUUikO0yKs7hj2fTP7S0'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Auth helpers
export const auth = {
  signUp: async (email, password, options = {}) => {
    return await supabase.auth.signUp({
      email,
      password,
      options
    })
  },
  
  signIn: async (email, password) => {
    return await supabase.auth.signInWithPassword({
      email,
      password
    })
  },
  
  signOut: async () => {
    return await supabase.auth.signOut()
  },
  
  getUser: async () => {
    return await supabase.auth.getUser()
  },
  
  getSession: async () => {
    return await supabase.auth.getSession()
  },
  
  onAuthStateChange: (callback) => {
    return supabase.auth.onAuthStateChange(callback)
  }
}

// Database helpers
export const db = {
  investigations: {
    create: async (investigation) => {
      return await supabase
        .from('investigations')
        .insert(investigation)
        .select()
    },
    
    getByUserId: async (userId) => {
      return await supabase
        .from('investigations')
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false })
    },
    
    getById: async (id) => {
      return await supabase
        .from('investigations')
        .select('*')
        .eq('id', id)
        .single()
    },
    
    update: async (id, updates) => {
      return await supabase
        .from('investigations')
        .update(updates)
        .eq('id', id)
        .select()
    }
  },
  
  profiles: {
    get: async (userId) => {
      return await supabase
        .from('profiles')
        .select('*')
        .eq('id', userId)
        .single()
    },
    
    update: async (userId, updates) => {
      return await supabase
        .from('profiles')
        .update(updates)
        .eq('id', userId)
        .select()
    }
  }
}

// Storage helpers
export const storage = {
  uploadFile: async (bucket, path, file) => {
    return await supabase.storage
      .from(bucket)
      .upload(path, file)
  },
  
  getPublicUrl: (bucket, path) => {
    return supabase.storage
      .from(bucket)
      .getPublicUrl(path)
  }
}