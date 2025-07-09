import React, { useEffect, useState } from 'react'
import { useInvestigation } from '../contexts/InvestigationContext'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/layout/Layout'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card'
import {
  Search, Plus, Filter, Eye, Clock, CheckCircle, XCircle,
  AlertTriangle, Globe, Mail, FileText, ChevronDown
} from 'lucide-react'
import { motion } from 'framer-motion'
import { formatDate } from '../lib/utils'

const Investigations = () => {
  const { investigations, loadInvestigations, loading } = useInvestigation()
  const navigate = useNavigate()
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [typeFilter, setTypeFilter] = useState('all')
  const [filteredInvestigations, setFilteredInvestigations] = useState([])

  useEffect(() => {
    loadInvestigations()
  }, [loadInvestigations])

  useEffect(() => {
    let filtered = investigations

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(inv => 
        inv.target_url?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        inv.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        inv.description?.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Filter by status
    if (statusFilter !== 'all') {
      filtered = filtered.filter(inv => inv.status === statusFilter)
    }

    // Filter by type
    if (typeFilter !== 'all') {
      filtered = filtered.filter(inv => inv.type === typeFilter)
    }

    setFilteredInvestigations(filtered)
  }, [investigations, searchTerm, statusFilter, typeFilter])

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-400" />
      case 'failed':
        return <XCircle className="w-4 h-4 text-red-400" />
      case 'pending':
      case 'running':
        return <Clock className="w-4 h-4 text-yellow-400" />
      default:
        return <AlertTriangle className="w-4 h-4 text-orange-400" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'text-green-400 bg-green-400/20'
      case 'failed':
        return 'text-red-400 bg-red-400/20'
      case 'pending':
      case 'running':
        return 'text-yellow-400 bg-yellow-400/20'
      default:
        return 'text-orange-400 bg-orange-400/20'
    }
  }

  const getTypeIcon = (type) => {
    switch (type) {
      case 'website':
        return <Globe className="w-4 h-4 text-blue-400" />
      case 'email':
        return <Mail className="w-4 h-4 text-green-400" />
      case 'document':
        return <FileText className="w-4 h-4 text-purple-400" />
      default:
        return <AlertTriangle className="w-4 h-4 text-gray-400" />
    }
  }

  const getRiskLevel = (score) => {
    if (score >= 80) return { level: 'High', color: 'text-red-400 bg-red-400/20' }
    if (score >= 50) return { level: 'Medium', color: 'text-yellow-400 bg-yellow-400/20' }
    return { level: 'Low', color: 'text-green-400 bg-green-400/20' }
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white mb-2">
                Investigations
              </h1>
              <p className="text-gray-300">
                Manage and monitor your fraud investigations
              </p>
            </div>
            <Button
              variant="gradient"
              onClick={() => navigate('/investigations/new')}
              className="mt-4 md:mt-0 flex items-center space-x-2"
            >
              <Plus className="w-4 h-4" />
              <span>New Investigation</span>
            </Button>
          </div>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="mb-8"
        >
          <Card className="bg-black/40 backdrop-blur-xl border-white/10">
            <CardContent className="p-6">
              <div className="flex flex-col md:flex-row gap-4">
                {/* Search */}
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <Input
                      type="text"
                      placeholder="Search investigations..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10 bg-white/5 border-white/10 text-white placeholder:text-gray-400 focus:border-orange-500/50"
                    />
                  </div>
                </div>
                
                {/* Status Filter */}
                <div className="min-w-[150px]">
                  <select
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value)}
                    className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-md text-white focus:border-orange-500/50 focus:outline-none"
                  >
                    <option value="all">All Status</option>
                    <option value="pending">Pending</option>
                    <option value="running">Running</option>
                    <option value="completed">Completed</option>
                    <option value="failed">Failed</option>
                  </select>
                </div>
                
                {/* Type Filter */}
                <div className="min-w-[150px]">
                  <select
                    value={typeFilter}
                    onChange={(e) => setTypeFilter(e.target.value)}
                    className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-md text-white focus:border-orange-500/50 focus:outline-none"
                  >
                    <option value="all">All Types</option>
                    <option value="website">Website</option>
                    <option value="email">Email</option>
                    <option value="document">Document</option>
                  </select>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Investigations List */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Card className="bg-black/40 backdrop-blur-xl border-white/10">
            <CardHeader>
              <CardTitle className="text-white">
                {filteredInvestigations.length} Investigation{filteredInvestigations.length !== 1 ? 's' : ''}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="space-y-4">
                  {[...Array(5)].map((_, i) => (
                    <div key={i} className="animate-pulse h-20 bg-white/10 rounded-lg"></div>
                  ))}
                </div>
              ) : filteredInvestigations.length === 0 ? (
                <div className="text-center py-12">
                  <AlertTriangle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-400 mb-4">
                    {searchTerm || statusFilter !== 'all' || typeFilter !== 'all'
                      ? 'No investigations found matching your filters'
                      : 'No investigations yet'
                    }
                  </p>
                  <Button
                    variant="gradient"
                    onClick={() => navigate('/investigations/new')}
                  >
                    Start First Investigation
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  {filteredInvestigations.map((investigation, index) => {
                    const risk = getRiskLevel(investigation.risk_score || 0)
                    return (
                      <motion.div
                        key={investigation.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.05 }}
                        className="p-6 bg-white/5 rounded-lg border border-white/10 hover:border-orange-500/30 transition-all duration-200 cursor-pointer"
                        onClick={() => navigate(`/investigations/${investigation.id}`)}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-3 mb-3">
                              {getTypeIcon(investigation.type)}
                              <span className="text-white font-medium text-lg">
                                {investigation.target_url || investigation.title || 'Investigation'}
                              </span>
                              <div className={`px-3 py-1 rounded-full text-sm ${getStatusColor(investigation.status)}`}>
                                <div className="flex items-center space-x-1">
                                  {getStatusIcon(investigation.status)}
                                  <span className="capitalize">{investigation.status}</span>
                                </div>
                              </div>
                              {investigation.risk_score !== undefined && (
                                <div className={`px-3 py-1 rounded-full text-sm ${risk.color}`}>
                                  {risk.level} Risk
                                </div>
                              )}
                            </div>
                            
                            {investigation.description && (
                              <p className="text-gray-400 mb-3">{investigation.description}</p>
                            )}
                            
                            <div className="flex items-center space-x-6 text-sm text-gray-400">
                              <span>Created: {formatDate(investigation.created_at)}</span>
                              <span>Type: {investigation.type}</span>
                              {investigation.progress !== undefined && (
                                <span>Progress: {investigation.progress}%</span>
                              )}
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-3">
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={(e) => {
                                e.stopPropagation()
                                navigate(`/investigations/${investigation.id}`)
                              }}
                              className="text-orange-400 hover:text-orange-300"
                            >
                              <Eye className="w-4 h-4 mr-1" />
                              View
                            </Button>
                          </div>
                        </div>
                      </motion.div>
                    )
                  })}
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </Layout>
  )
}

export default Investigations