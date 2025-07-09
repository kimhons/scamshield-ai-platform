import React from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card'
import { Button } from '../ui/button'
import { motion } from 'framer-motion'
import { Eye, Clock, AlertTriangle, CheckCircle, XCircle, ArrowRight } from 'lucide-react'
import { formatDate } from '../../lib/utils'
import { useNavigate } from 'react-router-dom'

const RecentInvestigations = ({ investigations = [], loading = false }) => {
  const navigate = useNavigate()

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-400" />
      case 'failed':
        return <XCircle className="w-4 h-4 text-red-400" />
      case 'pending':
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
        return 'text-yellow-400 bg-yellow-400/20'
      default:
        return 'text-orange-400 bg-orange-400/20'
    }
  }

  const getRiskLevel = (score) => {
    if (score >= 80) return { level: 'High', color: 'text-red-400 bg-red-400/20' }
    if (score >= 50) return { level: 'Medium', color: 'text-yellow-400 bg-yellow-400/20' }
    return { level: 'Low', color: 'text-green-400 bg-green-400/20' }
  }

  if (loading) {
    return (
      <Card className="bg-black/40 backdrop-blur-xl border-white/10">
        <CardHeader>
          <CardTitle className="text-white">Recent Investigations</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="h-16 bg-white/10 rounded-lg"></div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="bg-black/40 backdrop-blur-xl border-white/10">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-white">Recent Investigations</CardTitle>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => navigate('/investigations')}
          className="text-orange-400 hover:text-orange-300"
        >
          View All
          <ArrowRight className="w-4 h-4 ml-1" />
        </Button>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {investigations.length === 0 ? (
            <div className="text-center py-8">
              <AlertTriangle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-400">No investigations yet</p>
              <Button
                variant="gradient"
                onClick={() => navigate('/investigations/new')}
                className="mt-4"
              >
                Start First Investigation
              </Button>
            </div>
          ) : (
            investigations.slice(0, 5).map((investigation, index) => {
              const risk = getRiskLevel(investigation.risk_score || 0)
              return (
                <motion.div
                  key={investigation.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  className="p-4 bg-white/5 rounded-lg border border-white/10 hover:border-orange-500/30 transition-all duration-200 cursor-pointer"
                  onClick={() => navigate(`/investigations/${investigation.id}`)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <span className="text-white font-medium">
                          {investigation.target_url || investigation.title || 'Investigation'}
                        </span>
                        <div className={`px-2 py-1 rounded-full text-xs ${getStatusColor(investigation.status)}`}>
                          <div className="flex items-center space-x-1">
                            {getStatusIcon(investigation.status)}
                            <span className="capitalize">{investigation.status}</span>
                          </div>
                        </div>
                        {investigation.risk_score !== undefined && (
                          <div className={`px-2 py-1 rounded-full text-xs ${risk.color}`}>
                            {risk.level} Risk
                          </div>
                        )}
                      </div>
                      <p className="text-gray-400 text-sm">
                        {formatDate(investigation.created_at)}
                      </p>
                    </div>
                    <Eye className="w-5 h-5 text-gray-400 hover:text-orange-400 transition-colors" />
                  </div>
                </motion.div>
              )
            })
          )}
        </div>
      </CardContent>
    </Card>
  )
}

export default RecentInvestigations