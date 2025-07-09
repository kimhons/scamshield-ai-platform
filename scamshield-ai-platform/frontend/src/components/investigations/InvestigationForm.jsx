import React, { useState } from 'react'
import { useInvestigation } from '../../contexts/InvestigationContext'
import { useNavigate } from 'react-router-dom'
import { Button } from '../ui/button'
import { Input } from '../ui/input'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../ui/card'
import { Upload, Globe, Mail, FileText, AlertCircle, Zap } from 'lucide-react'
import { motion } from 'framer-motion'

const InvestigationForm = () => {
  const { createInvestigation, loading } = useInvestigation()
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    type: 'website',
    target_url: '',
    description: '',
    priority: 'normal'
  })
  const [files, setFiles] = useState([])
  const [error, setError] = useState('')

  const investigationTypes = [
    {
      id: 'website',
      name: 'Website Analysis',
      description: 'Analyze suspicious websites and domains',
      icon: Globe,
      color: 'from-blue-500 to-cyan-500'
    },
    {
      id: 'email',
      name: 'Email Investigation',
      description: 'Investigate phishing emails and scam messages',
      icon: Mail,
      color: 'from-green-500 to-emerald-500'
    },
    {
      id: 'document',
      name: 'Document Analysis',
      description: 'Analyze suspicious documents and files',
      icon: FileText,
      color: 'from-purple-500 to-pink-500'
    }
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (!formData.target_url && formData.type !== 'document') {
      setError('Target URL is required')
      return
    }

    if (formData.type === 'document' && files.length === 0) {
      setError('Please upload at least one file for document analysis')
      return
    }

    const investigationData = {
      ...formData,
      files: files.map(file => ({ name: file.name, size: file.size })),
      status: 'pending',
      progress: 0
    }

    const { data, error } = await createInvestigation(investigationData)

    if (error) {
      setError(error)
    } else {
      navigate(`/investigations/${data.id}`)
    }
  }

  const handleFileUpload = (e) => {
    const uploadedFiles = Array.from(e.target.files)
    setFiles(prev => [...prev, ...uploadedFiles])
  }

  const removeFile = (index) => {
    setFiles(prev => prev.filter((_, i) => i !== index))
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">
            Start New Investigation
          </h1>
          <p className="text-xl text-gray-300">
            Choose your investigation type and provide details
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Investigation Type Selection */}
          <Card className="bg-black/40 backdrop-blur-xl border-white/10">
            <CardHeader>
              <CardTitle className="text-white">Investigation Type</CardTitle>
              <CardDescription className="text-gray-400">
                Select the type of investigation you want to perform
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {investigationTypes.map((type) => {
                  const Icon = type.icon
                  const isSelected = formData.type === type.id
                  return (
                    <button
                      key={type.id}
                      type="button"
                      onClick={() => setFormData({ ...formData, type: type.id })}
                      className={`p-6 rounded-xl border-2 transition-all duration-300 text-left ${
                        isSelected
                          ? 'border-orange-500 bg-orange-500/20'
                          : 'border-white/10 bg-white/5 hover:border-white/20'
                      }`}
                    >
                      <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${type.color} flex items-center justify-center mb-4`}>
                        <Icon className="w-6 h-6 text-white" />
                      </div>
                      <h3 className="text-white font-semibold mb-2">{type.name}</h3>
                      <p className="text-gray-400 text-sm">{type.description}</p>
                    </button>
                  )
                })}
              </div>
            </CardContent>
          </Card>

          {/* Target Details */}
          <Card className="bg-black/40 backdrop-blur-xl border-white/10">
            <CardHeader>
              <CardTitle className="text-white">Target Details</CardTitle>
              <CardDescription className="text-gray-400">
                Provide the target URL or upload files for analysis
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {formData.type !== 'document' && (
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Target URL
                  </label>
                  <Input
                    type="url"
                    value={formData.target_url}
                    onChange={(e) => setFormData({ ...formData, target_url: e.target.value })}
                    placeholder="https://suspicious-website.com"
                    className="bg-white/5 border-white/10 text-white placeholder:text-gray-400 focus:border-orange-500/50"
                  />
                </div>
              )}

              {formData.type === 'document' && (
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Upload Files
                  </label>
                  <div className="border-2 border-dashed border-white/20 rounded-lg p-6 text-center hover:border-orange-500/50 transition-colors">
                    <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                    <p className="text-gray-400 mb-2">Drag and drop files here, or click to browse</p>
                    <input
                      type="file"
                      multiple
                      onChange={handleFileUpload}
                      className="hidden"
                      id="file-upload"
                      accept=".pdf,.doc,.docx,.txt,.jpg,.png,.jpeg"
                    />
                    <label htmlFor="file-upload">
                      <Button type="button" variant="outline" size="sm">
                        Choose Files
                      </Button>
                    </label>
                  </div>
                  
                  {files.length > 0 && (
                    <div className="mt-4 space-y-2">
                      {files.map((file, index) => (
                        <div key={index} className="flex items-center justify-between p-2 bg-white/5 rounded">
                          <span className="text-white text-sm">{file.name}</span>
                          <button
                            type="button"
                            onClick={() => removeFile(index)}
                            className="text-red-400 hover:text-red-300"
                          >
                            Remove
                          </button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Description (Optional)
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Describe what makes this suspicious or any additional context..."
                  rows={3}
                  className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-md text-white placeholder:text-gray-400 focus:border-orange-500/50 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Priority
                </label>
                <select
                  value={formData.priority}
                  onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                  className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-md text-white focus:border-orange-500/50 focus:outline-none"
                >
                  <option value="low">Low Priority</option>
                  <option value="normal">Normal Priority</option>
                  <option value="high">High Priority</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>
            </CardContent>
          </Card>

          {error && (
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center space-x-2 p-4 bg-red-500/20 border border-red-500/30 rounded-lg text-red-300"
            >
              <AlertCircle className="w-5 h-5" />
              <span>{error}</span>
            </motion.div>
          )}

          <div className="flex justify-end space-x-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate('/dashboard')}
              disabled={loading}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="gradient"
              size="lg"
              disabled={loading}
              className="min-w-[200px]"
            >
              {loading ? (
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Starting...</span>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <Zap className="w-4 h-4" />
                  <span>Start Investigation</span>
                </div>
              )}
            </Button>
          </div>
        </form>
      </motion.div>
    </div>
  )
}

export default InvestigationForm