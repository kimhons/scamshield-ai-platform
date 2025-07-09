import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, PieChart, Pie, Cell, AreaChart, Area, RadarChart, PolarGrid,
  PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';
import {
  Shield, AlertTriangle, TrendingUp, TrendingDown, Eye, Target, Zap, Brain,
  Activity, Users, Globe, Clock, DollarSign, Award, Search, FileText,
  BarChart3, PieChart as PieChartIcon, Settings, Filter, Download, RefreshCw,
  ChevronUp, ChevronDown, Play, Pause, MoreHorizontal, ArrowUpRight, ArrowDownRight
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Separator } from '../ui/separator';

// Enhanced Stats Card with animations
const EnhancedStatsCard = ({ title, value, change, changeType, icon: Icon, color, description, trend }) => {
  const [displayValue, setDisplayValue] = useState(0);
  
  useEffect(() => {
    const numericValue = typeof value === 'string' ? parseInt(value.replace(/[^0-9]/g, '')) : value;
    const timer = setTimeout(() => {
      setDisplayValue(numericValue);
    }, 100);
    return () => clearTimeout(timer);
  }, [value]);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      whileHover={{ y: -5, scale: 1.02 }}
      className="group"
    >
      <Card className="glass border-white/10 hover:border-primary/30 transition-all duration-500 overflow-hidden relative">
        {/* Gradient Background */}
        <div className={`absolute inset-0 bg-gradient-to-br ${color} opacity-5 group-hover:opacity-10 transition-opacity duration-500`} />
        
        <CardContent className="p-6 relative z-10">
          <div className="flex items-center justify-between mb-4">
            <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${color} p-3 shadow-glow`}>
              <Icon className="w-6 h-6 text-white" />
            </div>
            {change && (
              <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium ${
                changeType === 'up' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
              }`}>
                {changeType === 'up' ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
                <span>{change}</span>
              </div>
            )}
          </div>
          
          <div className="space-y-2">
            <motion.div 
              className="text-3xl font-bold text-foreground"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              {typeof value === 'string' ? value : displayValue.toLocaleString()}
            </motion.div>
            <div className="text-sm text-muted-foreground font-medium">{title}</div>
            {description && (
              <div className="text-xs text-muted-foreground">{description}</div>
            )}
          </div>
          
          {trend && (
            <div className="mt-4">
              <div className="flex justify-between text-xs text-muted-foreground mb-1">
                <span>Trend</span>
                <span>{trend}%</span>
              </div>
              <Progress value={Math.abs(trend)} className="h-1" />
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
};

// Real-time Activity Feed
const ActivityFeed = () => {
  const [activities, setActivities] = useState([
    {
      id: 1,
      type: 'threat_detected',
      message: 'High-risk phishing attempt blocked',
      timestamp: '2 minutes ago',
      severity: 'high',
      icon: Shield
    },
    {
      id: 2,
      type: 'investigation_completed',
      message: 'Investigation #2847 completed with 94% confidence',
      timestamp: '5 minutes ago',
      severity: 'success',
      icon: FileText
    },
    {
      id: 3,
      type: 'user_activity',
      message: '15 new users joined security monitoring',
      timestamp: '12 minutes ago',
      severity: 'info',
      icon: Users
    },
    {
      id: 4,
      type: 'ai_analysis',
      message: 'AI model updated with 2.3K new threat patterns',
      timestamp: '18 minutes ago',
      severity: 'info',
      icon: Brain
    }
  ]);

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high': return 'text-red-400 bg-red-500/20';
      case 'success': return 'text-green-400 bg-green-500/20';
      case 'info': return 'text-blue-400 bg-blue-500/20';
      default: return 'text-gray-400 bg-gray-500/20';
    }
  };

  return (
    <Card className="glass border-white/10 h-full">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-lg font-semibold">Real-time Activity</CardTitle>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span className="text-xs text-muted-foreground">Live</span>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <div className="max-h-80 overflow-y-auto">
          <AnimatePresence>
            {activities.map((activity, index) => (
              <motion.div
                key={activity.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ delay: index * 0.1 }}
                className="p-4 border-b border-white/5 hover:bg-white/5 transition-colors"
              >
                <div className="flex items-start space-x-3">
                  <div className={`w-8 h-8 rounded-lg p-2 ${getSeverityColor(activity.severity)}`}>
                    <activity.icon className="w-4 h-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-foreground">{activity.message}</p>
                    <p className="text-xs text-muted-foreground mt-1">{activity.timestamp}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </CardContent>
    </Card>
  );
};

// Advanced Analytics Chart
const AnalyticsChart = () => {
  const [timeRange, setTimeRange] = useState('7d');
  const [chartType, setChartType] = useState('threats');

  const threatsData = [
    { name: 'Mon', threats: 45, blocked: 43, severity: 8.2 },
    { name: 'Tue', threats: 52, blocked: 48, severity: 7.8 },
    { name: 'Wed', threats: 38, blocked: 36, severity: 6.5 },
    { name: 'Thu', threats: 67, blocked: 61, severity: 9.1 },
    { name: 'Fri', threats: 71, blocked: 68, severity: 8.9 },
    { name: 'Sat', threats: 29, blocked: 28, severity: 5.2 },
    { name: 'Sun', threats: 41, blocked: 39, severity: 7.3 }
  ];

  const performanceData = [
    { name: 'Detection Rate', value: 99.2, fill: '#f97316' },
    { name: 'False Positives', value: 0.8, fill: '#ef4444' }
  ];

  const radarData = [
    { subject: 'Phishing', A: 98, B: 92 },
    { subject: 'Malware', A: 95, B: 89 },
    { subject: 'Social Eng.', A: 89, B: 85 },
    { subject: 'Financial', A: 97, B: 94 },
    { subject: 'Identity', A: 93, B: 88 },
    { subject: 'Crypto', A: 91, B: 86 }
  ];

  return (
    <Card className="glass border-white/10 col-span-2">
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-lg font-semibold">Advanced Analytics</CardTitle>
          <p className="text-sm text-muted-foreground mt-1">
            Real-time threat detection and analysis metrics
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Tabs value={chartType} onValueChange={setChartType} className="w-auto">
            <TabsList className="grid w-full grid-cols-3 bg-muted/20">
              <TabsTrigger value="threats" className="text-xs">Threats</TabsTrigger>
              <TabsTrigger value="performance" className="text-xs">Performance</TabsTrigger>
              <TabsTrigger value="radar" className="text-xs">Coverage</TabsTrigger>
            </TabsList>
          </Tabs>
          <Button variant="outline" size="sm" className="h-8">
            <Download className="w-3 h-3 mr-1" />
            Export
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <AnimatePresence mode="wait">
            {chartType === 'threats' && (
              <motion.div
                key="threats"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="h-full"
              >
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={threatsData}>
                    <defs>
                      <linearGradient id="threatGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#f97316" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#f97316" stopOpacity={0}/>
                      </linearGradient>
                      <linearGradient id="blockedGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                    <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} />
                    <YAxis stroke="#9ca3af" fontSize={12} />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: 'rgba(0, 0, 0, 0.9)', 
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '8px',
                        color: 'white'
                      }} 
                    />
                    <Area 
                      type="monotone" 
                      dataKey="threats" 
                      stroke="#f97316" 
                      fillOpacity={1} 
                      fill="url(#threatGradient)" 
                      strokeWidth={2}
                    />
                    <Area 
                      type="monotone" 
                      dataKey="blocked" 
                      stroke="#10b981" 
                      fillOpacity={1} 
                      fill="url(#blockedGradient)" 
                      strokeWidth={2}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </motion.div>
            )}

            {chartType === 'performance' && (
              <motion.div
                key="performance"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="h-full flex items-center justify-center"
              >
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={performanceData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={120}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {performanceData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: 'rgba(0, 0, 0, 0.9)', 
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '8px',
                        color: 'white'
                      }} 
                    />
                  </PieChart>
                </ResponsiveContainer>
              </motion.div>
            )}

            {chartType === 'radar' && (
              <motion.div
                key="radar"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="h-full"
              >
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={radarData}>
                    <PolarGrid stroke="#374151" />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#9ca3af', fontSize: 12 }} />
                    <PolarRadiusAxis 
                      angle={0} 
                      domain={[0, 100]} 
                      tick={{ fill: '#9ca3af', fontSize: 10 }}
                    />
                    <Radar 
                      name="Current" 
                      dataKey="A" 
                      stroke="#f97316" 
                      fill="#f97316" 
                      fillOpacity={0.2} 
                      strokeWidth={2}
                    />
                    <Radar 
                      name="Previous" 
                      dataKey="B" 
                      stroke="#3b82f6" 
                      fill="#3b82f6" 
                      fillOpacity={0.1} 
                      strokeWidth={2}
                    />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: 'rgba(0, 0, 0, 0.9)', 
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '8px',
                        color: 'white'
                      }} 
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </CardContent>
    </Card>
  );
};

// Threat Intelligence Widget
const ThreatIntelligence = () => {
  const threats = [
    {
      id: 1,
      type: 'Phishing Campaign',
      severity: 'high',
      source: 'Email',
      targets: 1247,
      blocked: 1245,
      confidence: 94.2,
      timestamp: '2 min ago'
    },
    {
      id: 2,
      type: 'Deepfake Audio',
      severity: 'critical',
      source: 'Voice Call',
      targets: 43,
      blocked: 41,
      confidence: 98.7,
      timestamp: '8 min ago'
    },
    {
      id: 3,
      type: 'Social Engineering',
      severity: 'medium',
      source: 'Social Media',
      targets: 672,
      blocked: 659,
      confidence: 87.3,
      timestamp: '15 min ago'
    },
    {
      id: 4,
      type: 'Financial Scam',
      severity: 'high',
      source: 'SMS',
      targets: 892,
      blocked: 885,
      confidence: 91.8,
      timestamp: '22 min ago'
    }
  ];

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'bg-red-500/20 text-red-400 border-red-500/50';
      case 'high': return 'bg-orange-500/20 text-orange-400 border-orange-500/50';
      case 'medium': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50';
      case 'low': return 'bg-green-500/20 text-green-400 border-green-500/50';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/50';
    }
  };

  return (
    <Card className="glass border-white/10">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-lg font-semibold flex items-center">
          <AlertTriangle className="w-5 h-5 mr-2 text-primary" />
          Threat Intelligence
        </CardTitle>
        <Button variant="outline" size="sm" className="h-8">
          <RefreshCw className="w-3 h-3 mr-1" />
          Refresh
        </Button>
      </CardHeader>
      <CardContent className="p-0">
        <div className="max-h-96 overflow-y-auto">
          {threats.map((threat, index) => (
            <motion.div
              key={threat.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-4 border-b border-white/5 hover:bg-white/5 transition-colors"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <Badge className={`text-xs ${getSeverityColor(threat.severity)}`}>
                    {threat.severity.toUpperCase()}
                  </Badge>
                  <span className="text-sm font-medium text-foreground">{threat.type}</span>
                </div>
                <span className="text-xs text-muted-foreground">{threat.timestamp}</span>
              </div>
              
              <div className="grid grid-cols-2 gap-4 text-xs">
                <div>
                  <span className="text-muted-foreground">Source:</span>
                  <span className="text-foreground ml-1">{threat.source}</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Confidence:</span>
                  <span className="text-primary ml-1 font-medium">{threat.confidence}%</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Targets:</span>
                  <span className="text-foreground ml-1">{threat.targets.toLocaleString()}</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Blocked:</span>
                  <span className="text-green-400 ml-1 font-medium">{threat.blocked.toLocaleString()}</span>
                </div>
              </div>

              <div className="mt-3">
                <div className="flex justify-between text-xs text-muted-foreground mb-1">
                  <span>Success Rate</span>
                  <span>{((threat.blocked / threat.targets) * 100).toFixed(1)}%</span>
                </div>
                <Progress 
                  value={(threat.blocked / threat.targets) * 100} 
                  className="h-1"
                />
              </div>
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

// Main Premium Dashboard Component
const PremiumDashboard = () => {
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 2000);
  };

  const statsData = [
    {
      title: 'Active Investigations',
      value: '247',
      change: '+12.5%',
      changeType: 'up',
      icon: Search,
      color: 'from-primary to-orange-600',
      description: 'Currently processing',
      trend: 15.2
    },
    {
      title: 'Threats Detected',
      value: '1,843',
      change: '+8.3%',
      changeType: 'up',
      icon: AlertTriangle,
      color: 'from-red-500 to-red-600',
      description: 'Last 24 hours',
      trend: 8.3
    },
    {
      title: 'Success Rate',
      value: '99.2%',
      change: '+0.3%',
      changeType: 'up',
      icon: Target,
      color: 'from-green-500 to-green-600',
      description: 'Detection accuracy',
      trend: 99.2
    },
    {
      title: 'Response Time',
      value: '12.4s',
      change: '-2.1s',
      changeType: 'up',
      icon: Clock,
      color: 'from-blue-500 to-blue-600',
      description: 'Average response',
      trend: 85.7
    },
    {
      title: 'Protected Assets',
      value: '$2.8B',
      change: '+15.7%',
      changeType: 'up',
      icon: Shield,
      color: 'from-purple-500 to-purple-600',
      description: 'Total value secured',
      trend: 94.1
    },
    {
      title: 'AI Confidence',
      value: '96.8%',
      change: '+1.2%',
      changeType: 'up',
      icon: Brain,
      color: 'from-cyan-500 to-cyan-600',
      description: 'Model accuracy',
      trend: 96.8
    }
  ];

  return (
    <div className="min-h-screen bg-background p-6 space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col md:flex-row md:items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold gradient-text font-tech mb-2">
            Security Command Center
          </h1>
          <p className="text-muted-foreground">
            Real-time threat monitoring and AI-powered investigation dashboard
          </p>
        </div>
        <div className="flex items-center space-x-3 mt-4 md:mt-0">
          <Button 
            variant="outline" 
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="glass border-white/20"
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button className="bg-gradient-premium text-white hover:shadow-glow">
            <Settings className="w-4 h-4 mr-2" />
            Configure
          </Button>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
        {statsData.map((stat, index) => (
          <EnhancedStatsCard key={index} {...stat} />
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Analytics Chart - Takes up 2 columns */}
        <AnalyticsChart />
        
        {/* Activity Feed */}
        <ActivityFeed />
      </div>

      {/* Bottom Section */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* Threat Intelligence */}
        <ThreatIntelligence />
        
        {/* Additional Metrics or Recent Investigations could go here */}
        <Card className="glass border-white/10">
          <CardHeader>
            <CardTitle className="text-lg font-semibold flex items-center">
              <BarChart3 className="w-5 h-5 mr-2 text-primary" />
              Performance Metrics
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { label: 'Detection Speed', value: 92, color: 'bg-primary' },
                { label: 'False Positive Rate', value: 15, color: 'bg-red-500', inverted: true },
                { label: 'Investigation Quality', value: 88, color: 'bg-green-500' },
                { label: 'User Satisfaction', value: 95, color: 'bg-blue-500' },
                { label: 'System Uptime', value: 99.9, color: 'bg-purple-500' }
              ].map((metric, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="space-y-2"
                >
                  <div className="flex justify-between text-sm">
                    <span className="text-foreground">{metric.label}</span>
                    <span className="text-muted-foreground">{metric.value}%</span>
                  </div>
                  <div className="w-full bg-muted/20 rounded-full h-2 overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${metric.value}%` }}
                      transition={{ duration: 1, delay: index * 0.1 + 0.5 }}
                      className={`h-full ${metric.color} rounded-full transition-all duration-500`}
                    />
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default PremiumDashboard;
