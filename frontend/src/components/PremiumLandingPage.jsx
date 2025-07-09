import React, { useState, useEffect } from 'react';
import { 
  Shield, Zap, Brain, Users, CheckCircle, ArrowRight, Star, Globe, TrendingUp, 
  AlertTriangle, Eye, Target, Cpu, Database, Lock, Scale, FileText, 
  Award, Gavel, BookOpen, Search, Clock, DollarSign, Layers, 
  BarChart3, Microscope, ShieldCheck, UserCheck, FileCheck,
  Verified, AlertCircle, Info, ExternalLink, Crown, Sparkles,
  ChevronDown, Play, Rocket, Flame, Zap as Lightning
} from 'lucide-react';

const PremiumLandingPage = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [activeRegion, setActiveRegion] = useState('global');

  useEffect(() => {
    setIsVisible(true);
  }, []);

  // Global fraud statistics by region
  const fraudStats = {
    global: [
      { number: "$5.8T", label: "Global Fraud Losses (2024)", trend: "+23%" },
      { number: "2.8B", label: "People Targeted Annually", trend: "+45%" },
      { number: "300%", label: "AI Scam Increase", trend: "+300%" },
      { number: "15 min", label: "Avg Time to Lose Money", trend: "-50%" }
    ],
    northAmerica: [
      { number: "$2.1T", label: "North America Losses", trend: "+18%" },
      { number: "890M", label: "People Targeted", trend: "+32%" },
      { number: "$12,500", label: "Average Loss per Victim", trend: "+28%" },
      { number: "67%", label: "AI-Generated Scams", trend: "+400%" }
    ],
    europe: [
      { number: "$1.4T", label: "European Union Losses", trend: "+25%" },
      { number: "650M", label: "People Targeted", trend: "+38%" },
      { number: "$8,900", label: "Average Loss per Victim", trend: "+22%" },
      { number: "72%", label: "Cross-Border Fraud", trend: "+55%" }
    ],
    asia: [
      { number: "$1.8T", label: "Asia-Pacific Losses", trend: "+31%" },
      { number: "1.1B", label: "People Targeted", trend: "+52%" },
      { number: "$6,200", label: "Average Loss per Victim", trend: "+19%" },
      { number: "89%", label: "Mobile-Based Scams", trend: "+78%" }
    ]
  };

  const aiThreatStats = [
    {
      icon: Brain,
      title: "Deepfake Voice Cloning",
      stat: "2,400%",
      description: "Increase in voice cloning scams targeting families and businesses",
      color: "from-red-500 to-pink-500"
    },
    {
      icon: Eye,
      title: "AI-Generated Identities",
      stat: "890%",
      description: "Rise in completely fabricated personas for romance and investment scams",
      color: "from-orange-500 to-red-500"
    },
    {
      icon: FileText,
      title: "Synthetic Documents",
      stat: "1,200%",
      description: "AI-created fake documents, contracts, and official communications",
      color: "from-purple-500 to-pink-500"
    },
    {
      icon: Target,
      title: "Personalized Attacks",
      stat: "650%",
      description: "AI analyzing social media to create hyper-targeted scam campaigns",
      color: "from-blue-500 to-purple-500"
    }
  ];

  const regionData = [
    { id: 'global', name: 'Global', flag: '🌍' },
    { id: 'northAmerica', name: 'North America', flag: '🇺🇸' },
    { id: 'europe', name: 'Europe', flag: '🇪🇺' },
    { id: 'asia', name: 'Asia-Pacific', flag: '🌏' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiM5QzkyQUMiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMSIvPjwvZz48L2c+PC9zdmc+')] opacity-20"></div>
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-blue-600/10 via-purple-600/10 to-pink-600/10 animate-pulse"></div>
        
        {/* Floating particles */}
        <div className="absolute top-20 left-10 w-2 h-2 bg-orange-500 rounded-full animate-bounce opacity-60"></div>
        <div className="absolute top-40 right-20 w-3 h-3 bg-blue-500 rounded-full animate-pulse opacity-40"></div>
        <div className="absolute bottom-40 left-20 w-2 h-2 bg-purple-500 rounded-full animate-bounce opacity-50"></div>
        <div className="absolute bottom-20 right-10 w-3 h-3 bg-pink-500 rounded-full animate-pulse opacity-60"></div>
      </div>

      {/* Header */}
      <header className="relative z-50 bg-black/20 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <Shield className="h-10 w-10 text-orange-500" />
                <div className="absolute inset-0 h-10 w-10 text-orange-500 animate-pulse opacity-50"></div>
              </div>
              <div>
                <span className="text-2xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">ScamShield</span>
                <span className="text-2xl font-bold bg-gradient-to-r from-orange-500 to-yellow-500 bg-clip-text text-transparent ml-1">AI</span>
              </div>
            </div>
            
            <nav className="hidden md:flex space-x-8">
              <a href="#crisis" className="text-gray-300 hover:text-white transition-all duration-300 hover:scale-105">The Crisis</a>
              <a href="#solution" className="text-gray-300 hover:text-white transition-all duration-300 hover:scale-105">Solution</a>
              <a href="#pricing" className="text-gray-300 hover:text-white transition-all duration-300 hover:scale-105">Pricing</a>
              <a href="#demo" className="text-gray-300 hover:text-white transition-all duration-300 hover:scale-105">Demo</a>
            </nav>
            
            <div className="flex items-center space-x-4">
              <button className="text-gray-300 hover:text-white transition-all duration-300">Sign In</button>
              <button className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-6 py-3 rounded-xl font-semibold hover:from-orange-600 hover:to-red-600 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-orange-500/25">
                <Rocket className="w-4 h-4 inline mr-2" />
                Start Investigation
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative z-10 pt-20 pb-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="mb-8">
            <div className="inline-flex items-center bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-blue-500/30 rounded-full px-6 py-3 mb-8">
              <Sparkles className="w-5 h-5 text-blue-400 mr-2" />
              <span className="text-blue-300 font-semibold">🚀 Now Available: AI-Powered Fraud Detection</span>
            </div>
          </div>
          
          <h1 className={`text-6xl md:text-8xl font-bold mb-8 transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
            <span className="bg-gradient-to-r from-white via-gray-100 to-white bg-clip-text text-transparent">
              Detect Fraud
            </span>
            <br />
            <span className="bg-gradient-to-r from-orange-500 via-red-500 to-pink-500 bg-clip-text text-transparent">
              With AI Precision
            </span>
          </h1>
          
          <p className={`text-xl md:text-2xl text-gray-300 mb-12 max-w-4xl mx-auto leading-relaxed transition-all duration-1000 delay-300 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
            Advanced AI-powered fraud detection platform. Investigate suspicious websites, emails, and schemes with technology designed to identify modern scam tactics.
          </p>
          
          <div className={`flex flex-col sm:flex-row gap-6 justify-center items-center transition-all duration-1000 delay-500 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
            <button className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-8 py-4 rounded-xl text-lg font-semibold hover:from-orange-600 hover:to-red-600 transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-orange-500/25 flex items-center">
              <Lightning className="w-6 h-6 mr-2" />
              Try ScamShield AI - Free
              <ArrowRight className="w-5 h-5 ml-2" />
            </button>
            <button className="border-2 border-white/30 text-white px-8 py-4 rounded-xl text-lg font-semibold hover:bg-white/10 transition-all duration-300 transform hover:scale-105 backdrop-blur-sm flex items-center">
              <Play className="w-5 h-5 mr-2" />
              Watch Demo
            </button>
          </div>
          
          <div className="mt-16 flex justify-center items-center space-x-8 text-gray-400">
            <div className="flex items-center">
              <Shield className="w-5 h-5 text-green-500 mr-1" />
              <span>Advanced AI Detection</span>
            </div>
            <div className="flex items-center">
              <Database className="w-5 h-5 text-blue-500 mr-1" />
              <span>50+ Data Sources</span>
            </div>
            <div className="flex items-center">
              <Lightning className="w-5 h-5 text-orange-500 mr-1" />
              <span>Instant Results</span>
            </div>
          </div>
        </div>
      </section>

      {/* Global Fraud Crisis Section */}
      <section id="crisis" className="relative z-10 py-20 bg-black/20 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-bold mb-6">
              <span className="bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent">
                The Global Fraud Crisis
              </span>
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Fraud has reached epidemic proportions worldwide. AI is making it worse, faster, and more sophisticated than ever before.
            </p>
          </div>

          {/* Region Selector */}
          <div className="flex justify-center mb-12">
            <div className="bg-black/30 backdrop-blur-md rounded-2xl p-2 border border-white/10">
              <div className="flex space-x-2">
                {regionData.map((region) => (
                  <button
                    key={region.id}
                    onClick={() => setActiveRegion(region.id)}
                    className={`px-6 py-3 rounded-xl font-semibold transition-all duration-300 flex items-center space-x-2 ${
                      activeRegion === region.id
                        ? 'bg-gradient-to-r from-orange-500 to-red-500 text-white shadow-lg'
                        : 'text-gray-300 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    <span className="text-lg">{region.flag}</span>
                    <span>{region.name}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Regional Statistics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
            {fraudStats[activeRegion].map((stat, index) => (
              <div key={index} className="bg-gradient-to-br from-black/40 to-black/20 backdrop-blur-md rounded-2xl p-8 border border-white/10 hover:border-orange-500/30 transition-all duration-300 transform hover:scale-105">
                <div className="text-center">
                  <div className="text-4xl font-bold bg-gradient-to-r from-orange-500 to-red-500 bg-clip-text text-transparent mb-2">
                    {stat.number}
                  </div>
                  <div className="text-gray-300 mb-3">{stat.label}</div>
                  <div className="inline-flex items-center bg-red-500/20 text-red-300 px-3 py-1 rounded-full text-sm">
                    <TrendingUp className="w-4 h-4 mr-1" />
                    {stat.trend}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* AI Threat Statistics */}
          <div className="mb-16">
            <h3 className="text-3xl font-bold text-center mb-12">
              <span className="bg-gradient-to-r from-purple-500 to-pink-500 bg-clip-text text-transparent">
                AI is Making Fraud Exponentially Worse
              </span>
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {aiThreatStats.map((threat, index) => (
                <div key={index} className="bg-gradient-to-br from-black/40 to-black/20 backdrop-blur-md rounded-2xl p-8 border border-white/10 hover:border-purple-500/30 transition-all duration-300 transform hover:scale-105">
                  <div className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${threat.color} flex items-center justify-center mb-6 mx-auto`}>
                    <threat.icon className="w-8 h-8 text-white" />
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-2">
                      +{threat.stat}
                    </div>
                    <div className="text-lg font-semibold text-white mb-3">{threat.title}</div>
                    <div className="text-gray-400 text-sm">{threat.description}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Problem Statement */}
          <div className="bg-gradient-to-r from-red-500/20 to-orange-500/20 border border-red-500/30 rounded-3xl p-12 text-center">
            <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-6" />
            <h3 className="text-3xl font-bold text-white mb-4">
              The Fraud Epidemic is Real
            </h3>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              With $5.8 trillion lost to fraud globally in 2024 and AI making scams more sophisticated than ever, you need advanced protection. ScamShield AI gives you the tools to fight back.
            </p>
            <button className="bg-gradient-to-r from-red-500 to-orange-500 text-white px-8 py-4 rounded-xl text-lg font-semibold hover:from-red-600 hover:to-orange-600 transition-all duration-300 transform hover:scale-105 shadow-2xl">
              <Shield className="w-6 h-6 mr-2 inline" />
              Start Your First Investigation
            </button>
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section id="solution" className="relative z-10 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-bold mb-6">
              <span className="bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">
                How ScamShield AI Works
              </span>
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              ScamShield AI uses multiple AI models and data sources to analyze potential fraud and provide detailed investigation reports.
            </p>
          </div>

          {/* Feature Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            <div className="bg-gradient-to-br from-black/40 to-black/20 backdrop-blur-md rounded-2xl p-8 border border-white/10 hover:border-blue-500/30 transition-all duration-300 transform hover:scale-105">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center mb-6">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-4">Multi-AI Analysis</h3>
              <p className="text-gray-400">Multiple AI models work together to analyze websites, emails, and documents for signs of fraud and deception.</p>
            </div>

            <div className="bg-gradient-to-br from-black/40 to-black/20 backdrop-blur-md rounded-2xl p-8 border border-white/10 hover:border-green-500/30 transition-all duration-300 transform hover:scale-105">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-r from-green-500 to-emerald-500 flex items-center justify-center mb-6">
                <Database className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-4">Comprehensive Data</h3>
              <p className="text-gray-400">Access to 50+ public databases and APIs for thorough background checks and verification.</p>
            </div>

            <div className="bg-gradient-to-br from-black/40 to-black/20 backdrop-blur-md rounded-2xl p-8 border border-white/10 hover:border-orange-500/30 transition-all duration-300 transform hover:scale-105">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-r from-orange-500 to-red-500 flex items-center justify-center mb-6">
                <Lightning className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-4">Fast Results</h3>
              <p className="text-gray-400">Get detailed investigation reports quickly, helping you make informed decisions about potential threats.</p>
            </div>
          </div>

          {/* CTA Section */}
          <div className="text-center">
            <button className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-12 py-6 rounded-2xl text-xl font-bold hover:from-blue-600 hover:to-purple-600 transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-blue-500/25">
              <Crown className="w-6 h-6 mr-3 inline" />
              Start Your Investigation
              <ArrowRight className="w-6 h-6 ml-3 inline" />
            </button>
          </div>
        </div>
      </section>

      {/* Footer with Fine Print */}
      <footer className="relative z-10 bg-black/40 backdrop-blur-md border-t border-white/10 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
            <div>
              <div className="flex items-center space-x-3 mb-6">
                <Shield className="h-8 w-8 text-orange-500" />
                <span className="text-xl font-bold text-white">ScamShield AI</span>
              </div>
              <p className="text-gray-400">
                Advanced AI-powered fraud detection and investigation platform.
              </p>
            </div>
            
            <div>
              <h4 className="text-white font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-white font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Support</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-white font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Ethical Guidelines</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Legal Framework</a></li>
              </ul>
            </div>
          </div>
          
          {/* Fine Print Legal Disclaimers */}
          <div className="border-t border-white/10 pt-8">
            <div className="text-xs text-gray-500 space-y-2">
              <p>
                <strong>Important Legal Notice:</strong> ScamShield AI provides evidence-based analysis for informational purposes only. 
                Users are responsible for independent verification of all information and their own decisions based on our reports. 
                We present facts and evidence, not legal determinations or accusations.
              </p>
              <p>
                <strong>Ethical Framework:</strong> Our platform prioritizes ethical responsibility, legal compliance, and evidence-based analysis. 
                All findings are backed by verifiable sources with reliability scoring. We maintain the highest professional standards 
                preventing harm, respecting privacy, and ensuring responsible use.
              </p>
              <p>
                <strong>Disclaimer:</strong> While we strive for accuracy, no fraud detection system is 100% perfect. 
                Users should always exercise caution and seek professional advice for legal or financial matters. 
                ScamShield AI is not liable for decisions made based on our analysis.
              </p>
            </div>
            
            <div className="flex flex-col md:flex-row justify-between items-center mt-8 pt-8 border-t border-white/10">
              <p className="text-gray-400 text-sm">
                © 2025 ScamShield AI. All rights reserved. Evidence-based fraud investigation platform.
              </p>
              <div className="flex items-center space-x-4 mt-4 md:mt-0">
                <span className="text-gray-400 text-sm">Ethical AI • Legal Compliance • Professional Standards</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default PremiumLandingPage;

