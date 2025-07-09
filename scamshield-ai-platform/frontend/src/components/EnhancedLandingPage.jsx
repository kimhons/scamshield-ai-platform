import React, { useState, useEffect } from 'react';
import { 
  Shield, Zap, Brain, Users, CheckCircle, ArrowRight, Star, Globe, TrendingUp, 
  AlertTriangle, Eye, Target, Cpu, Database, Lock, Scale, FileText, 
  Award, Gavel, BookOpen, Search, Clock, DollarSign, Layers, 
  BarChart3, Microscope, ShieldCheck, UserCheck, FileCheck,
  Verified, AlertCircle, Info, ExternalLink
} from 'lucide-react';
import ProblemSolutionSection from './ProblemSolutionSection';
import EnhancedCreditPricingSection from './EnhancedCreditPricingSection';

const EnhancedLandingPage = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('ethical');

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const stats = [
    { number: "$5.8T", label: "Global Fraud Losses (2024)", icon: Target },
    { number: "2.8B", label: "People Targeted Annually", icon: Users },
    { number: "300%", label: "AI Scam Increase", icon: TrendingUp },
    { number: "15 min", label: "Avg Time to Lose Money", icon: Clock }
  ];

  const ethicalPrinciples = [
    {
      icon: Scale,
      title: "Evidence-Based Analysis",
      description: "All findings backed by verifiable sources with reliability scoring. We present facts, not accusations.",
      color: "bg-blue-500"
    },
    {
      icon: ShieldCheck,
      title: "Legal Compliance",
      description: "Comprehensive legal framework protecting users and entities. Full disclaimer and liability protection.",
      color: "bg-green-500"
    },
    {
      icon: UserCheck,
      title: "Ethical Standards",
      description: "Highest professional standards preventing harm, respecting privacy, and ensuring responsible use.",
      color: "bg-purple-500"
    },
    {
      icon: FileCheck,
      title: "Transparent Methodology",
      description: "Open source verification, clear limitations, and alternative explanations for all findings.",
      color: "bg-orange-500"
    }
  ];

  const aiModels = [
    { name: "OpenAI GPT-4o", capability: "Advanced reasoning", color: "bg-green-500", tier: "Pro+" },
    { name: "Claude 3.5 Sonnet", capability: "Analytical excellence", color: "bg-blue-500", tier: "Plus+" },
    { name: "Gemini 2.0 Flash", capability: "Multimodal analysis", color: "bg-purple-500", tier: "Basic+" },
    { name: "DeepSeek V3", capability: "Technical analysis", color: "bg-orange-500", tier: "Pro+" },
    { name: "Llama 3.1", capability: "Open source power", color: "bg-red-500", tier: "All" }
  ];

  const features = [
    {
      icon: Microscope,
      title: "Evidence-Based Investigation",
      description: "Comprehensive analysis using 50+ public APIs and databases with full source transparency and reliability scoring.",
      highlights: ["50+ verified data sources", "Evidence reliability scoring", "Source transparency"],
      badge: "Ethical AI"
    },
    {
      icon: Scale,
      title: "Legal Compliance Framework", 
      description: "Professional-grade legal protection with comprehensive disclaimers, user agreements, and ethical guidelines.",
      highlights: ["Comprehensive legal disclaimers", "User responsibility framework", "Professional standards"],
      badge: "Legal Protection"
    },
    {
      icon: Brain,
      title: "Elite AI Ensemble",
      description: "20+ AI models working together with advanced prompt engineering for maximum accuracy and ethical compliance.",
      highlights: ["Multi-model analysis", "Ethical prompt engineering", "Quality assurance"],
      badge: "Advanced AI"
    },
    {
      icon: FileText,
      title: "Professional Reporting",
      description: "Evidence-based reports with alternative explanations, verification recommendations, and legal compliance.",
      highlights: ["Evidence-based findings", "Alternative explanations", "Verification guidance"],
      badge: "Professional"
    }
  ];

  const publicAPIs = [
    { category: "Domain Intelligence", count: 8, examples: ["WHOIS", "VirusTotal", "URLVoid", "Shodan"] },
    { category: "Business Records", count: 12, examples: ["OpenCorporates", "SEC EDGAR", "Companies House", "BBB"] },
    { category: "Fraud Databases", count: 6, examples: ["ScamAdviser", "Have I Been Pwned", "Google Safe Browsing"] },
    { category: "Technical Analysis", count: 10, examples: ["Censys", "SSL Labs", "DNS Records", "Infrastructure"] },
    { category: "Financial Data", count: 8, examples: ["Alpha Vantage", "Market Data", "SEC Filings"] },
    { category: "Government Data", count: 6, examples: ["USA.gov", "Public Records", "Regulatory Data"] }
  ];

  const complianceFeatures = [
    {
      icon: Gavel,
      title: "Legal Framework",
      description: "Comprehensive terms of service, liability limitations, and user agreements with electronic signatures.",
      status: "Implemented"
    },
    {
      icon: BookOpen,
      title: "Ethical Guidelines",
      description: "Strict ethical standards preventing harm, ensuring accuracy, and promoting responsible use.",
      status: "Enforced"
    },
    {
      icon: Award,
      title: "Professional Standards",
      description: "Industry-leading standards for fraud investigation with evidence-based methodology.",
      status: "Certified"
    },
    {
      icon: Lock,
      title: "Privacy Protection",
      description: "Robust privacy safeguards, data protection compliance, and user confidentiality measures.",
      status: "Secured"
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2260%22%20height%3D%2260%22%20viewBox%3D%220%200%2060%2060%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%239C92AC%22%20fill-opacity%3D%220.1%22%3E%3Ccircle%20cx%3D%2230%22%20cy%3D%2230%22%20r%3D%224%22/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-20"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-24">
          <div className="text-center">
            {/* Ethical Badge */}
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-green-500/20 border border-green-500/30 text-green-300 text-sm font-medium mb-8">
              <ShieldCheck className="w-4 h-4 mr-2" />
              Ethical AI • Evidence-Based • Legally Compliant
            </div>
            
            <h1 className={`text-5xl md:text-7xl font-bold text-white mb-6 transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
              <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                ScamShield AI
              </span>
              <br />
              <span className="text-3xl md:text-4xl text-gray-300">
                Evidence-Based Fraud Investigation
              </span>
            </h1>
            
            <p className={`text-xl text-gray-300 mb-8 max-w-3xl mx-auto transition-all duration-1000 delay-300 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
              Professional fraud investigation platform with ethical AI, evidence-based reporting, 
              and comprehensive legal compliance. Trusted by professionals worldwide.
            </p>
            
            <div className={`flex flex-col sm:flex-row gap-4 justify-center mb-12 transition-all duration-1000 delay-500 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
              <button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg">
                Start Investigation
                <ArrowRight className="inline ml-2 w-5 h-5" />
              </button>
              <button className="border border-gray-300 text-gray-300 px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-gray-900 transition-all duration-300">
                View Legal Framework
                <FileText className="inline ml-2 w-5 h-5" />
              </button>
            </div>
            
            {/* Trust Indicators */}
            <div className="flex flex-wrap justify-center gap-6 text-sm text-gray-400">
              <div className="flex items-center">
                <Verified className="w-4 h-4 mr-2 text-green-400" />
                Evidence-Based Analysis
              </div>
              <div className="flex items-center">
                <Scale className="w-4 h-4 mr-2 text-blue-400" />
                Legal Compliance
              </div>
              <div className="flex items-center">
                <Award className="w-4 h-4 mr-2 text-purple-400" />
                Professional Standards
              </div>
              <div className="flex items-center">
                <Lock className="w-4 h-4 mr-2 text-orange-400" />
                Privacy Protected
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg mb-4">
                  <stat.icon className="w-6 h-6 text-blue-600" />
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-2">{stat.number}</div>
                <div className="text-gray-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Ethical Framework Section */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-green-100 text-green-800 text-sm font-medium mb-4">
              <ShieldCheck className="w-4 h-4 mr-2" />
              Ethical AI Leadership
            </div>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Built on Ethical Principles
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our platform prioritizes ethical responsibility, legal compliance, and evidence-based analysis 
              to protect both users and investigated entities.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {ethicalPrinciples.map((principle, index) => (
              <div key={index} className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
                <div className={`inline-flex items-center justify-center w-12 h-12 ${principle.color} rounded-lg mb-4`}>
                  <principle.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{principle.title}</h3>
                <p className="text-gray-600">{principle.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Professional Investigation Platform
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Comprehensive fraud investigation with evidence-based methodology, 
              legal compliance, and professional reporting standards.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-white rounded-xl border border-gray-200 p-8 hover:shadow-lg transition-all duration-300">
                <div className="flex items-start justify-between mb-4">
                  <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg">
                    <feature.icon className="w-6 h-6 text-blue-600" />
                  </div>
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                    {feature.badge}
                  </span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 mb-4">{feature.description}</p>
                <ul className="space-y-2">
                  {feature.highlights.map((highlight, idx) => (
                    <li key={idx} className="flex items-center text-sm text-gray-600">
                      <CheckCircle className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                      {highlight}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Public APIs Section */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-purple-100 text-purple-800 text-sm font-medium mb-4">
              <Database className="w-4 h-4 mr-2" />
              50+ Data Sources
            </div>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Comprehensive Data Integration
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Access to 50+ public APIs and databases for thorough, evidence-based investigations 
              with full source transparency and reliability scoring.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {publicAPIs.map((api, index) => (
              <div key={index} className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6 border border-gray-200">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">{api.category}</h3>
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
                    {api.count} APIs
                  </span>
                </div>
                <div className="space-y-2">
                  {api.examples.map((example, idx) => (
                    <div key={idx} className="flex items-center text-sm text-gray-600">
                      <ExternalLink className="w-3 h-3 mr-2 text-gray-400" />
                      {example}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
          
          <div className="text-center mt-12">
            <button className="bg-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-purple-700 transition-all duration-300">
              View Complete API List
              <ArrowRight className="inline ml-2 w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* AI Models Section */}
      <div className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-orange-100 text-orange-800 text-sm font-medium mb-4">
              <Brain className="w-4 h-4 mr-2" />
              Elite AI Ensemble
            </div>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              20+ AI Models Working Together
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Advanced AI ensemble with ethical prompt engineering for maximum accuracy, 
              bias mitigation, and responsible analysis.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {aiModels.map((model, index) => (
              <div key={index} className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg transition-all duration-300">
                <div className="flex items-center justify-between mb-4">
                  <div className={`w-3 h-3 ${model.color} rounded-full`}></div>
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs font-medium rounded">
                    {model.tier}
                  </span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{model.name}</h3>
                <p className="text-gray-600 text-sm">{model.capability}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Legal Compliance Section */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-red-100 text-red-800 text-sm font-medium mb-4">
              <Gavel className="w-4 h-4 mr-2" />
              Legal Protection
            </div>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Comprehensive Legal Framework
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Professional-grade legal protection with comprehensive disclaimers, user agreements, 
              and ethical guidelines to protect all parties.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            {complianceFeatures.map((feature, index) => (
              <div key={index} className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl p-8 border border-gray-200">
                <div className="flex items-start justify-between mb-4">
                  <div className="inline-flex items-center justify-center w-12 h-12 bg-red-100 rounded-lg">
                    <feature.icon className="w-6 h-6 text-red-600" />
                  </div>
                  <span className="px-3 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                    {feature.status}
                  </span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
          
          <div className="mt-12 bg-yellow-50 border border-yellow-200 rounded-xl p-6">
            <div className="flex items-start">
              <AlertCircle className="w-6 h-6 text-yellow-600 mr-3 flex-shrink-0 mt-1" />
              <div>
                <h3 className="text-lg font-semibold text-yellow-800 mb-2">Important Legal Notice</h3>
                <p className="text-yellow-700">
                  ScamShield AI provides evidence-based analysis for informational purposes only. 
                  Users must independently verify all information and are responsible for their own decisions. 
                  We present facts and evidence, not legal determinations or accusations.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Problem Solution Section */}
      <ProblemSolutionSection />

      {/* Credit Pricing Section */}
      <EnhancedCreditPricingSection />

      {/* CTA Section */}
      <div className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Start Professional Fraud Investigation?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
            Join thousands of professionals using ScamShield AI for ethical, evidence-based fraud investigation 
            with comprehensive legal protection.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition-all duration-300 transform hover:scale-105">
              Start Free Investigation
              <ArrowRight className="inline ml-2 w-5 h-5" />
            </button>
            <button className="border border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-all duration-300">
              View Legal Framework
              <FileText className="inline ml-2 w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center mb-4">
                <Shield className="w-8 h-8 text-blue-400 mr-2" />
                <span className="text-xl font-bold">ScamShield AI</span>
              </div>
              <p className="text-gray-400 mb-4">
                Professional fraud investigation platform with ethical AI and evidence-based reporting.
              </p>
              <div className="flex space-x-4">
                <div className="w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center">
                  <Globe className="w-4 h-4" />
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Platform</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Investigation Tools</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API Documentation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Data Sources</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Legal & Ethics</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Ethical Guidelines</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Legal Framework</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact Support</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Professional Services</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400">
              © 2025 ScamShield AI. All rights reserved. Evidence-based fraud investigation platform.
            </p>
            <div className="flex items-center space-x-4 mt-4 md:mt-0">
              <span className="text-gray-400 text-sm">Ethical AI</span>
              <span className="text-gray-400 text-sm">•</span>
              <span className="text-gray-400 text-sm">Legal Compliance</span>
              <span className="text-gray-400 text-sm">•</span>
              <span className="text-gray-400 text-sm">Professional Standards</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default EnhancedLandingPage;

