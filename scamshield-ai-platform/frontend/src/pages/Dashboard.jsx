import React, { useEffect, useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useInvestigation } from '../contexts/InvestigationContext'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/layout/Layout'
import StatsCard from '../components/dashboard/StatsCard'
import RecentInvestigations from '../components/dashboard/RecentInvestigations'
import { Button } from '../components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card'
import {
  Shield, Search, AlertTriangle, TrendingUp, Zap, Plus,
  Brain, Database, Clock, CheckCircle
} from 'lucide-react'
import { motion } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const Dashboard = () => {
  const { user } = useAuth()
  const { investigations, loadInvestigations, loading } = useInvestigation()
  const navigate = useNavigate()
  const [stats, setStats] = useState({
    totalInvestigations: 0,
    activeInvestigations: 0,
    threatsDetected: 0,
    riskScore: 0
  })

  useEffect(() => {
    loadInvestigations()
  }, [loadInvestigations])

  useEffect(() => {
    if (investigations.length > 0) {
      const active = investigations.filter(inv => inv.status === 'pending' || inv.status === 'running').length
      const threats = investigations.filter(inv => inv.risk_score && inv.risk_score > 70).length
      const avgRisk = investigations.reduce((acc, inv) => acc + (inv.risk_score || 0), 0) / investigations.length
      
      setStats({
        totalInvestigations: investigations.length,
        activeInvestigations: active,
        threatsDetected: threats,
        riskScore: Math.round(avgRisk)
      })
    }
  }, [investigations])

  const statsCards = [
    {
      title: 'Total Investigations',
      value: stats.totalInvestigations.toString(),
      change: '+12%',
      icon: Search,
      gradient: 'from-blue-500 to-cyan-500'
    },
    {
      title: 'Active Investigations',
      value: stats.activeInvestigations.toString(),
      change: '+5%',
      icon: Clock,
      gradient: 'from-yellow-500 to-orange-500'
    },
    {
      title: 'Threats Detected',
      value: stats.threatsDetected.toString(),
      change: '-8%',
      icon: AlertTriangle,
      gradient: 'from-red-500 to-pink-500'
    },
    {
      title: 'Avg Risk Score',
      value: `${stats.riskScore}%`,
      change: '+3%',
      icon: TrendingUp,
      gradient: 'from-purple-500 to-indigo-500'
    }
  ]

  // Mock data for charts
  const weeklyData = [
    { name: 'Mon', investigations: 4, threats: 2 },
    { name: 'Tue', investigations: 6, threats: 1 },
    { name: 'Wed', investigations: 8, threats: 3 },
    { name: 'Thu', investigations: 5, threats: 2 },
    { name: 'Fri', investigations: 7, threats: 1 },
    { name: 'Sat', investigations: 3, threats: 0 },
    { name: 'Sun', investigations: 2, threats: 0 }
  ]

  const riskDistribution = [
    { name: 'Low Risk', value: 60, color: '#10B981' },
    { name: 'Medium Risk', value: 25, color: '#F59E0B' },
    { name: 'High Risk', value: 15, color: '#EF4444' }
  ]

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white mb-2">
                Welcome back, {user?.user_metadata?.full_name || user?.email?.split('@')[0] || 'User'}!
              </h1>
              <p className="text-gray-300">
                Monitor your fraud investigations and stay protected with AI-powered analysis.
              </p>
            </div>
            <div className="mt-4 md:mt-0 flex space-x-3">
              <Button
                variant="gradient"
                onClick={() => navigate('/investigations/new')}
                className="flex items-center space-x-2"
              >
                <Plus className="w-4 h-4" />
                <span>New Investigation</span>
              </Button>
              <Button
                variant="outline"
                onClick={() => navigate('/investigations')}
                className="border-white/20 text-white hover:bg-white/10"
              >
                <Search className="w-4 h-4 mr-2" />
                View All
              </Button>
            </div>
          </div>
        </motion.div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statsCards.map((stat, index) => (
            <StatsCard key={stat.title} {...stat} index={index} />
          ))}
        </div>

        {/* Charts and Recent Investigations */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Weekly Activity Chart */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <Card className="bg-black/40 backdrop-blur-xl border-white/10">
              <CardHeader>
                <CardTitle className="text-white flex items-center space-x-2">
                  <BarChart className="w-5 h-5" />
                  <span>Weekly Activity</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={weeklyData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="name" stroke="#9CA3AF" />
                    <YAxis stroke="#9CA3AF" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '8px',
                        color: '#fff'
                      }}
                    />
                    <Bar dataKey="investigations" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="threats" fill="#EF4444" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </motion.div>

          {/* Risk Distribution */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            <Card className="bg-black/40 backdrop-blur-xl border-white/10">
              <CardHeader>
                <CardTitle className="text-white flex items-center space-x-2">
                  <PieChart className="w-5 h-5" />
                  <span>Risk Distribution</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={riskDistribution}
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {riskDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '8px',
                        color: '#fff'
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Recent Investigations */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
        >
          <RecentInvestigations investigations={investigations} loading={loading} />
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.7 }}
          className="mt-8"
        >
          <Card className="bg-black/40 backdrop-blur-xl border-white/10">
            <CardHeader>
              <CardTitle className="text-white">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Button
                  variant="outline"
                  onClick={() => navigate('/investigations/new?type=website')}
                  className="h-16 border-white/20 text-white hover:bg-white/10 flex items-center space-x-3"
                >
                  <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
                    <Shield className="w-4 h-4 text-white" />
                  </div>
                  <span>Analyze Website</span>
                </Button>
                
                <Button
                  variant="outline"
                  onClick={() => navigate('/investigations/new?type=email')}
                  className="h-16 border-white/20 text-white hover:bg-white/10 flex items-center space-x-3"
                >
                  <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                    <Brain className="w-4 h-4 text-white" />
                  </div>
                  <span>Check Email</span>
                </Button>
                
                <Button
                  variant="outline"
                  onClick={() => navigate('/investigations/new?type=document')}
                  className="h-16 border-white/20 text-white hover:bg-white/10 flex items-center space-x-3"
                >
                  <div className="w-8 h-8 bg-purple-500 rounded-lg flex items-center justify-center">
                    <Database className="w-4 h-4 text-white" />
                  </div>
                  <span>Scan Document</span>
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </Layout>
  )
}

export default Dashboard