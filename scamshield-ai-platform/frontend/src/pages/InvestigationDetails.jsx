import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useInvestigation } from '../contexts/InvestigationContext'
import Layout from '../components/layout/Layout'
import { Button } from '../components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card'
import { Progress } from '../components/ui/progress'
import {
  ArrowLeft, Clock, CheckCircle, XCircle, AlertTriangle,
  Globe, Mail, FileText, Download, Share, RefreshCw,
  Shield, Eye, Zap, Database, Brain
} from 'lucide-react'
import { motion } from 'framer-motion'
import { formatDate } from '../lib/utils'

const InvestigationDetails = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { currentInvestigation, loadInvestigation, loading } = useInvestigation()
  const [analysis, setAnalysis] = useState(null)
  const [analysisLoading, setAnalysisLoading] = useState(false)

  useEffect(() => {
    if (id) {
      loadInvestigation(id)
    }
  }, [id, loadInvestigation])

  // Mock analysis results
  useEffect(() => {
    if (currentInvestigation && currentInvestigation.status === 'completed') {
      setAnalysis({
        riskScore: currentInvestigation.risk_score || 75,
        findings: [
          {
            category: 'Domain Analysis',
            status: 'warning',
            description: 'Domain registered recently (less than 30 days)',
            severity: 'medium'
          },
          {
            category: 'SSL Certificate',
            status: 'success',
            description: 'Valid SSL certificate from trusted authority',
            severity: 'low'
          },
          {
            category: 'Content Analysis',
            status: 'danger',
            description: 'Contains suspicious keywords and phrases',
            severity: 'high'
          },
          {
            category: 'Reputation Check',
            status: 'warning',
            description: 'Limited reputation data available',
            severity: 'medium'
          }
        ],
        recommendations: [
          'Exercise extreme caution when interacting with this website',
          'Verify the legitimacy through official channels',
          'Do not provide personal or financial information',
          'Report suspicious activity to relevant authorities'
        ],
        technicalDetails: {
          ipAddress: '192.168.1.1',
          location: 'Unknown',
          registrar: 'Example Registrar',
          whoisData: 'Limited WHOIS information available'
        }
      })
    }
  }, [currentInvestigation])

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-400" />
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-400" />
      case 'pending':
      case 'running':
        return <Clock className="w-5 h-5 text-yellow-400" />
      default:
        return <AlertTriangle className="w-5 h-5 text-orange-400" />
    }
  }

  const getTypeIcon = (type) => {
    switch (type) {
      case 'website':
        return <Globe className="w-5 h-5" />
      case 'email':
        return <Mail className="w-5 h-5" />
      case 'document':
        return <FileText className="w-5 h-5" />
      default:
        return <Shield className="w-5 h-5" />
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high':
        return 'text-red-400 bg-red-400/20'
      case 'medium':
        return 'text-yellow-400 bg-yellow-400/20'
      case 'low':
        return 'text-green-400 bg-green-400/20'
      default:
        return 'text-gray-400 bg-gray-400/20'
    }
  }

  const getFindingIcon = (status) => {
    switch (status) {
      case 'success':
        return <CheckCircle className="w-4 h-4 text-green-400" />
      case 'warning':
        return <AlertTriangle className="w-4 h-4 text-yellow-400" />
      case 'danger':
        return <XCircle className="w-4 h-4 text-red-400" />
      default:
        return <Eye className="w-4 h-4 text-gray-400" />
    }
  }

  if (loading || !currentInvestigation) {
    return (
      <Layout>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-pulse space-y-8">
            <div className="h-8 bg-white/10 rounded w-1/3"></div>
            <div className="h-64 bg-white/10 rounded"></div>
            <div className="h-64 bg-white/10 rounded"></div>
          </div>
        </div>
      </Layout>
    )
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
          <Button
            variant="ghost"
            onClick={() => navigate('/investigations')}
            className="mb-4 text-gray-300 hover:text-white"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Investigations
          </Button>
          
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white mb-2">
                Investigation Details
              </h1>
              <p className="text-gray-300">
                {currentInvestigation.target_url || currentInvestigation.title || 'Investigation'}
              </p>
            </div>
            <div className="mt-4 md:mt-0 flex space-x-3">
              <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
                <Download className="w-4 h-4 mr-2" />
                Export Report
              </Button>
              <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
                <Share className="w-4 h-4 mr-2" />
                Share
              </Button>
            </div>
          </div>
        </motion.div>

        {/* Investigation Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="mb-8"
        >
          <Card className="bg-black/40 backdrop-blur-xl border-white/10">
            <CardHeader>
              <CardTitle className="text-white flex items-center space-x-2">
                {getTypeIcon(currentInvestigation.type)}
                <span>Investigation Overview</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div>
                  <p className="text-gray-400 text-sm mb-1">Status</p>
                  <div className="flex items-center space-x-2">
                    {getStatusIcon(currentInvestigation.status)}
                    <span className="text-white capitalize">{currentInvestigation.status}</span>
                  </div>
                </div>
                <div>
                  <p className="text-gray-400 text-sm mb-1">Type</p>
                  <p className="text-white capitalize">{currentInvestigation.type}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm mb-1">Created</p>
                  <p className="text-white">{formatDate(currentInvestigation.created_at)}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm mb-1">Progress</p>
                  <div className="space-y-2">
                    <Progress value={currentInvestigation.progress || 0} className="h-2" />
                    <p className="text-white text-sm">{currentInvestigation.progress || 0}%</p>
                  </div>
                </div>
              </div>
              
              {currentInvestigation.description && (
                <div className="mt-6">
                  <p className="text-gray-400 text-sm mb-2">Description</p>
                  <p className="text-white">{currentInvestigation.description}</p>
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>

        {/* Analysis Results */}
        {analysis && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            {/* Risk Assessment */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <Card className="bg-black/40 backdrop-blur-xl border-white/10">
                <CardHeader>
                  <CardTitle className="text-white flex items-center space-x-2">
                    <Shield className="w-5 h-5" />
                    <span>Risk Assessment</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center mb-6">
                    <div className={`inline-flex items-center justify-center w-24 h-24 rounded-full text-2xl font-bold ${
                      analysis.riskScore >= 80 ? 'bg-red-500/20 text-red-400' :
                      analysis.riskScore >= 50 ? 'bg-yellow-500/20 text-yellow-400' :
                      'bg-green-500/20 text-green-400'
                    }`}>
                      {analysis.riskScore}%
                    </div>
                    <p className={`mt-2 font-medium ${
                      analysis.riskScore >= 80 ? 'text-red-400' :
                      analysis.riskScore >= 50 ? 'text-yellow-400' :
                      'text-green-400'
                    }`}>
                      {analysis.riskScore >= 80 ? 'High Risk' :
                       analysis.riskScore >= 50 ? 'Medium Risk' : 'Low Risk'}
                    </p>
                  </div>
                  
                  <div className="space-y-4">
                    <h4 className="text-white font-semibold">Recommendations</h4>
                    <ul className="space-y-2">
                      {analysis.recommendations.map((rec, index) => (
                        <li key={index} className="flex items-start space-x-2">
                          <div className="w-1.5 h-1.5 bg-orange-500 rounded-full mt-2 flex-shrink-0" />
                          <span className="text-gray-300 text-sm">{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Findings */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              <Card className="bg-black/40 backdrop-blur-xl border-white/10">
                <CardHeader>
                  <CardTitle className="text-white flex items-center space-x-2">
                    <Brain className="w-5 h-5" />
                    <span>Analysis Findings</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {analysis.findings.map((finding, index) => (
                      <div key={index} className="p-4 bg-white/5 rounded-lg border border-white/10">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            {getFindingIcon(finding.status)}
                            <span className="text-white font-medium">{finding.category}</span>
                          </div>
                          <div className={`px-2 py-1 rounded-full text-xs ${getSeverityColor(finding.severity)}`}>
                            {finding.severity.toUpperCase()}
                          </div>
                        </div>
                        <p className="text-gray-300 text-sm">{finding.description}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        )}

        {/* Technical Details */}
        {analysis?.technicalDetails && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <Card className="bg-black/40 backdrop-blur-xl border-white/10">
              <CardHeader>
                <CardTitle className="text-white flex items-center space-x-2">
                  <Database className="w-5 h-5" />
                  <span>Technical Details</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <p className="text-gray-400 text-sm mb-1">IP Address</p>
                    <p className="text-white font-mono">{analysis.technicalDetails.ipAddress}</p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm mb-1">Location</p>
                    <p className="text-white">{analysis.technicalDetails.location}</p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm mb-1">Registrar</p>
                    <p className="text-white">{analysis.technicalDetails.registrar}</p>
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm mb-1">WHOIS Data</p>
                    <p className="text-white">{analysis.technicalDetails.whoisData}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>
    </Layout>
  )
}

export default InvestigationDetails