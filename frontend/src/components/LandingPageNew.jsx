import React, { useState, useEffect } from 'react';
import { Shield, Zap, Brain, Users, CheckCircle, ArrowRight, Star, Globe, TrendingUp, AlertTriangle, Eye, Target, Cpu, Database, Lock } from 'lucide-react';
import ProblemSolutionSection from './ProblemSolutionSection';
import CreditPricingSection from './CreditPricingSection';

const LandingPage = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const stats = [
    { number: "$5.8T", label: "Global Fraud Losses (2024)", icon: Target },
    { number: "2.8B", label: "People Targeted Annually", icon: DollarSign },
    { number: "300%", label: "AI Scam Increase", icon: Search },
    { number: "15 min", label: "Avg Time to Lose Money", icon: Clock }
  ];

  const aiModels = [
    { name: "OpenAI GPT-4o", capability: "Advanced reasoning", color: "bg-green-500" },
    { name: "Claude 3.5 Sonnet", capability: "Analytical excellence", color: "bg-blue-500" },
    { name: "Gemini 2.0 Flash", capability: "Multimodal analysis", color: "bg-purple-500" },
    { name: "DeepSeek V3", capability: "Technical analysis", color: "bg-orange-500" },
    { name: "Llama 3.1", capability: "Open source power", color: "bg-red-500" }
  ];

  const features = [
    {
      icon: Search,
      title: "Multi-Modal Analysis",
      description: "Analyze URLs, emails, images, documents, phone numbers, social media profiles, IP addresses, and cryptocurrency addresses with AI precision.",
      highlights: ["Domain & WHOIS analysis", "Image metadata extraction", "Social engineering detection"]
    },
    {
      icon: Layers,
      title: "Intelligence Fusion", 
      description: "Correlate threats across multiple sources, identify threat actors, and predict emerging fraud patterns with advanced AI.",
      highlights: ["Threat attribution analysis", "Pattern recognition", "Predictive modeling"]
    },
    {
      icon: Zap,
      title: "Real-Time Processing",
      description: "Get instant results with our optimized AI pipeline. Average investigation time: 15 seconds.",
      highlights: ["Instant threat correlation", "Live progress tracking", "Comprehensive reporting"]
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Shield className="h-8 w-8 text-blue-600 mr-2" />
              <span className="text-xl font-bold text-gray-900">ScamShield AI</span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-600 hover:text-gray-900 transition-colors">Features</a>
              <a href="#pricing" className="text-gray-600 hover:text-gray-900 transition-colors">Pricing</a>
              <a href="#about" className="text-gray-600 hover:text-gray-900 transition-colors">About</a>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                Get Started
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className={`text-center transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
            <div className="flex justify-center mb-8">
              <div className="relative">
                <div className="bg-blue-100 rounded-full p-4">
                  <Shield className="h-16 w-16 text-blue-600" />
                </div>
                <div className="absolute -top-2 -right-2">
                  <Sparkles className="h-8 w-8 text-yellow-500 animate-bounce" />
                </div>
              </div>
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              Stop the <span className="text-red-600">$5.8 Trillion</span> Fraud Crisis
              <br />
              <span className="text-blue-600">Elite AI Investigation</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-600 mb-4 max-w-4xl mx-auto">
              <span className="text-red-600 font-bold">2.8 billion people</span> are targeted by scams annually. 
              Traditional security fails against AI-powered fraud.
            </p>
            
            <p className="text-lg md:text-xl text-gray-600 mb-8 max-w-4xl mx-auto">
              Professional-grade fraud detection with <span className="text-blue-600 font-semibold">FBI/CIA-level capabilities</span>. 
              Born from a real $500 scam, now protecting millions worldwide.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl">
                Start Free Investigation
                <ArrowRight className="inline ml-2 h-5 w-5" />
              </button>
              <button className="border-2 border-gray-300 text-gray-700 hover:bg-gray-50 px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300 flex items-center justify-center">
                <Play className="h-5 w-5 mr-2" />
                Watch Demo
              </button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="flex justify-center mb-2">
                    <div className="bg-blue-100 rounded-lg p-2">
                      <stat.icon className="h-6 w-6 text-blue-600" />
                    </div>
                  </div>
                  <div className="text-3xl font-bold text-gray-900 mb-1">{stat.number}</div>
                  <div className="text-gray-600 text-sm">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Problem & Solution Section */}
      <ProblemSolutionSection />

      {/* AI Models Showcase */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Powered by <span className="text-blue-600">20+ Elite AI Models</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              The most comprehensive AI arsenal ever assembled for fraud detection, 
              combining the best proprietary and open-source models.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
            {aiModels.map((model, index) => (
              <div key={index} className="bg-white border border-gray-200 rounded-xl p-6 text-center hover:shadow-lg transition-all duration-300 hover:transform hover:scale-105">
                <div className={`w-12 h-12 ${model.color} rounded-full mx-auto mb-4 flex items-center justify-center`}>
                  <Brain className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-gray-900 font-semibold mb-2">{model.name}</h3>
                <p className="text-gray-600 text-sm">{model.capability}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div id="features" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Elite Investigation Capabilities
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Analyze any digital artifact with intelligence-grade precision
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-white rounded-xl p-8 shadow-sm border border-gray-200 hover:shadow-lg transition-all duration-300">
                <div className="bg-blue-100 rounded-lg p-3 w-fit mb-6">
                  <feature.icon className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">{feature.title}</h3>
                <p className="text-gray-600 mb-6">{feature.description}</p>
                <ul className="space-y-2">
                  {feature.highlights.map((highlight, idx) => (
                    <li key={idx} className="flex items-center text-gray-700">
                      <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
                      {highlight}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Pricing Section */}
      <CreditPricingSection />

      {/* Technology & Security */}
      <div className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Built by <span className="text-blue-600">Fraud Victims</span>, For Everyone
            </h2>
            <p className="text-xl text-gray-600">
              Born from a real $500 scam experience, ScamShield AI combines cutting-edge technology with real-world understanding of fraud tactics.
            </p>
          </div>

          <div className="bg-gray-50 rounded-xl p-8 text-center border border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div>
                <div className="bg-blue-100 rounded-lg p-3 w-fit mx-auto mb-4">
                  <Brain className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">20+ AI Models</h3>
                <p className="text-gray-600">Most comprehensive AI arsenal for fraud detection</p>
              </div>
              
              <div>
                <div className="bg-green-100 rounded-lg p-3 w-fit mx-auto mb-4">
                  <Zap className="h-8 w-8 text-green-600" />
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">Real-Time Analysis</h3>
                <p className="text-gray-600">Instant threat detection and correlation</p>
              </div>
              
              <div>
                <div className="bg-purple-100 rounded-lg p-3 w-fit mx-auto mb-4">
                  <Shield className="h-8 w-8 text-purple-600" />
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">Enterprise Security</h3>
                <p className="text-gray-600">Bank-grade security and compliance</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20 bg-blue-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Stop Fraud Before It Happens?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join thousands of security professionals using ScamShield AI to protect their organizations. 
            Start your free investigation today.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300 transform hover:scale-105 shadow-lg">
              Start Free Investigation
              <ArrowRight className="inline ml-2 h-5 w-5" />
            </button>
            <button className="border-2 border-white text-white hover:bg-white hover:text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300">
              Schedule Demo
            </button>
          </div>

          <div className="mt-8 text-blue-100">
            <p className="text-sm">
              ✓ 14-day free trial ✓ No credit card required ✓ Setup in 5 minutes
            </p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center mb-4">
                <Shield className="h-8 w-8 text-blue-400 mr-2" />
                <span className="text-xl font-bold text-white">ScamShield AI</span>
              </div>
              <p className="text-gray-400 mb-4">
                Elite AI-powered fraud investigation platform protecting millions worldwide.
              </p>
              <div className="flex space-x-4">
                <div className="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center">
                  <Globe className="h-4 w-4 text-gray-400" />
                </div>
                <div className="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center">
                  <Users className="h-4 w-4 text-gray-400" />
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-white font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
              </ul>
            </div>

            <div>
              <h3 className="text-white font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
              </ul>
            </div>

            <div>
              <h3 className="text-white font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Security</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 ScamShield AI. All rights reserved. Born from a $500 scam, now protecting millions.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;

