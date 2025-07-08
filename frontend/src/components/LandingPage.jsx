import React, { useState, useEffect } from 'react';
import { 
  Shield, 
  Zap, 
  Brain, 
  Eye, 
  CheckCircle, 
  Star, 
  ArrowRight, 
  Users, 
  Globe, 
  Lock,
  TrendingUp,
  Award,
  Sparkles,
  Target,
  Layers,
  Cpu,
  Search,
  AlertTriangle,
  DollarSign,
  Clock,
  BarChart3
} from 'lucide-react';

const LandingPage = () => {
  const [activeTab, setActiveTab] = useState('basic');
  const [isVisible, setIsVisible] = useState(false);
  const [currentTestimonial, setCurrentTestimonial] = useState(0);

  useEffect(() => {
    setIsVisible(true);
    const interval = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const pricingTiers = [
    {
      id: 'basic',
      name: 'Basic',
      price: '$19.99',
      period: '/month',
      credits: '10 credits included',
      creditValue: '$0.35 each additional',
      description: 'Perfect for individuals and small businesses',
      features: [
        'Quick scam detection',
        'Basic fraud analysis',
        'Community database access',
        'Email support',
        'Mobile app access',
        'Basic reporting'
      ],
      highlight: false,
      color: 'from-blue-500 to-cyan-500'
    },
    {
      id: 'professional',
      name: 'Professional',
      price: '$89.99',
      period: '/month',
      credits: '25 credits included',
      creditValue: '$1.85 each additional',
      description: 'Advanced AI analysis for professionals',
      features: [
        'Advanced AI investigation',
        'Behavioral profiling',
        'Multi-modal analysis',
        'Priority support',
        'API access',
        'Advanced reporting',
        'Team collaboration',
        'Custom alerts'
      ],
      highlight: true,
      color: 'from-purple-500 to-pink-500'
    },
    {
      id: 'enterprise',
      name: 'Enterprise',
      price: '$399.99',
      period: '/month',
      credits: '100 credits included',
      creditValue: '$7.25 each additional',
      description: 'Elite AI ensemble for large organizations',
      features: [
        'Elite AI ensemble',
        'Strategic intelligence',
        'Threat attribution',
        'Dedicated support',
        'Custom integrations',
        'White-label options',
        'Advanced analytics',
        'Compliance reporting',
        'SLA guarantees'
      ],
      highlight: false,
      color: 'from-orange-500 to-red-500'
    },
    {
      id: 'intelligence',
      name: 'Intelligence',
      price: '$1,999.99',
      period: '/month',
      credits: '250 credits included',
      creditValue: '$17.00 each additional',
      description: 'Maximum AI capabilities for intelligence agencies',
      features: [
        'Maximum AI capabilities',
        'Predictive modeling',
        'White-glove analysis',
        '24/7 dedicated support',
        'Custom AI training',
        'Government compliance',
        'Real-time intelligence',
        'Executive briefings',
        'Custom deployment'
      ],
      highlight: false,
      color: 'from-emerald-500 to-teal-500'
    }
  ];

  const testimonials = [
    {
      name: "Sarah Chen",
      role: "Cybersecurity Director",
      company: "TechCorp Industries",
      content: "ScamShield AI saved our company $2.3M by detecting a sophisticated business email compromise before any funds were transferred. The AI analysis was incredibly detailed.",
      rating: 5
    },
    {
      name: "Detective Mike Rodriguez",
      role: "Financial Crimes Unit",
      company: "Metro Police Department",
      content: "This platform has revolutionized our fraud investigations. What used to take weeks now takes hours, and the accuracy is phenomenal.",
      rating: 5
    },
    {
      name: "Jennifer Walsh",
      role: "Risk Management VP",
      company: "Global Financial Services",
      content: "The Enterprise tier gives us FBI-level investigation capabilities. We've prevented over $50M in fraud losses since implementation.",
      rating: 5
    }
  ];

  const stats = [
    { number: "99.9%", label: "Fraud Detection Accuracy", icon: Target },
    { number: "$500M+", label: "Fraud Prevented", icon: DollarSign },
    { number: "2.3M+", label: "Investigations Completed", icon: Search },
    { number: "15 sec", label: "Average Analysis Time", icon: Clock }
  ];

  const aiModels = [
    { name: "OpenAI GPT-4o", capability: "Advanced reasoning", color: "bg-green-500" },
    { name: "Claude 3.5 Sonnet", capability: "Analytical excellence", color: "bg-blue-500" },
    { name: "Gemini 2.0 Flash", capability: "Multimodal analysis", color: "bg-purple-500" },
    { name: "DeepSeek V3", capability: "Technical analysis", color: "bg-orange-500" },
    { name: "Llama 3.1", capability: "Open source power", color: "bg-red-500" }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-purple-600/20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className={`text-center transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
            <div className="flex justify-center mb-8">
              <div className="relative">
                <Shield className="h-20 w-20 text-cyan-400 animate-pulse" />
                <div className="absolute -top-2 -right-2">
                  <Sparkles className="h-8 w-8 text-yellow-400 animate-bounce" />
                </div>
              </div>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
              <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                ScamShield AI
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-4xl mx-auto">
              Elite AI-powered fraud investigation platform with <span className="text-cyan-400 font-semibold">FBI/CIA-level capabilities</span>. 
              Born from a real scam experience, now protecting millions.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <button className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl">
                Start Free Investigation
                <ArrowRight className="inline ml-2 h-5 w-5" />
              </button>
              <button className="border-2 border-purple-400 text-purple-400 hover:bg-purple-400 hover:text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300">
                Watch Demo
              </button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="flex justify-center mb-2">
                    <stat.icon className="h-8 w-8 text-cyan-400" />
                  </div>
                  <div className="text-3xl font-bold text-white mb-1">{stat.number}</div>
                  <div className="text-gray-400 text-sm">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* AI Models Showcase */}
      <div className="py-20 bg-slate-800/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Powered by <span className="text-cyan-400">20+ Elite AI Models</span>
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              The most comprehensive AI arsenal ever assembled for fraud detection, 
              combining the best proprietary and open-source models.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
            {aiModels.map((model, index) => (
              <div key={index} className="bg-slate-700/50 backdrop-blur-sm rounded-xl p-6 text-center hover:transform hover:scale-105 transition-all duration-300">
                <div className={`w-12 h-12 ${model.color} rounded-full mx-auto mb-4 flex items-center justify-center`}>
                  <Brain className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-white font-semibold mb-2">{model.name}</h3>
                <p className="text-gray-400 text-sm">{model.capability}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Elite Investigation Capabilities
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Analyze any digital artifact with intelligence-grade precision
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-8 hover:transform hover:scale-105 transition-all duration-300">
              <div className="bg-cyan-500/20 rounded-lg p-3 w-fit mb-6">
                <Search className="h-8 w-8 text-cyan-400" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-4">Multi-Modal Analysis</h3>
              <p className="text-gray-300 mb-6">
                Analyze URLs, emails, images, documents, phone numbers, social media profiles, 
                IP addresses, and cryptocurrency addresses with AI precision.
              </p>
              <ul className="space-y-2">
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
                  Domain & WHOIS analysis
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
                  Image metadata extraction
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
                  Social engineering detection
                </li>
              </ul>
            </div>

            <div className="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-8 hover:transform hover:scale-105 transition-all duration-300">
              <div className="bg-purple-500/20 rounded-lg p-3 w-fit mb-6">
                <Layers className="h-8 w-8 text-purple-400" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-4">Intelligence Fusion</h3>
              <p className="text-gray-300 mb-6">
                Correlate threats across multiple sources, identify threat actors, 
                and predict emerging fraud patterns with advanced AI.
              </p>
              <ul className="space-y-2">
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
                  Threat attribution analysis
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
                  Pattern recognition
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
                  Predictive modeling
                </li>
              </ul>
            </div>

            <div className="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-8 hover:transform hover:scale-105 transition-all duration-300">
              <div className="bg-orange-500/20 rounded-lg p-3 w-fit mb-6">
                <Zap className="h-8 w-8 text-orange-400" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-4">Real-Time Processing</h3>
              <p className="text-gray-300 mb-6">
                Get instant results with our optimized AI pipeline. 
                Average investigation time: 15 seconds.
              </p>
              <ul className="space-y-2">
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
                  Instant threat correlation
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
                  Live progress tracking
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
                  Comprehensive reporting
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Pricing Section */}
      <div className="py-20 bg-slate-800/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Choose Your <span className="text-cyan-400">Investigation Tier</span>
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              From basic scam detection to elite intelligence analysis. 
              50% profit margin ensures sustainable, high-quality service.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {pricingTiers.map((tier) => (
              <div 
                key={tier.id}
                className={`relative bg-slate-700/50 backdrop-blur-sm rounded-xl p-8 transition-all duration-300 hover:transform hover:scale-105 ${
                  tier.highlight ? 'ring-2 ring-purple-400 shadow-2xl shadow-purple-500/25' : ''
                }`}
              >
                {tier.highlight && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-full text-sm font-semibold">
                      Most Popular
                    </span>
                  </div>
                )}

                <div className={`bg-gradient-to-r ${tier.color} rounded-lg p-3 w-fit mb-6`}>
                  <Shield className="h-8 w-8 text-white" />
                </div>

                <h3 className="text-2xl font-bold text-white mb-2">{tier.name}</h3>
                <p className="text-gray-400 mb-6">{tier.description}</p>

                <div className="mb-6">
                  <span className="text-4xl font-bold text-white">{tier.price}</span>
                  <span className="text-gray-400">{tier.period}</span>
                </div>

                <div className="mb-6">
                  <div className="text-cyan-400 font-semibold mb-1">{tier.credits}</div>
                  <div className="text-gray-400 text-sm">{tier.creditValue}</div>
                </div>

                <ul className="space-y-3 mb-8">
                  {tier.features.map((feature, index) => (
                    <li key={index} className="flex items-center text-gray-300">
                      <CheckCircle className="h-5 w-5 text-green-400 mr-3 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>

                <button 
                  className={`w-full py-3 rounded-lg font-semibold transition-all duration-300 ${
                    tier.highlight 
                      ? 'bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white' 
                      : 'bg-slate-600 hover:bg-slate-500 text-white'
                  }`}
                >
                  Get Started
                </button>
              </div>
            ))}
          </div>

          <div className="text-center mt-12">
            <p className="text-gray-400 mb-4">
              All plans include 14-day free trial • No setup fees • Cancel anytime
            </p>
            <p className="text-sm text-gray-500">
              Enterprise and Intelligence tiers include custom deployment options and dedicated support
            </p>
          </div>
        </div>
      </div>

      {/* Testimonials */}
      <div className="py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Trusted by <span className="text-cyan-400">Security Professionals</span>
            </h2>
            <p className="text-xl text-gray-300">
              Real results from real customers protecting their organizations
            </p>
          </div>

          <div className="relative">
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8 text-center">
              <div className="flex justify-center mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-6 w-6 text-yellow-400 fill-current" />
                ))}
              </div>
              
              <blockquote className="text-xl text-gray-300 mb-6 italic">
                "{testimonials[currentTestimonial].content}"
              </blockquote>
              
              <div className="text-white font-semibold">
                {testimonials[currentTestimonial].name}
              </div>
              <div className="text-gray-400">
                {testimonials[currentTestimonial].role}, {testimonials[currentTestimonial].company}
              </div>
            </div>

            <div className="flex justify-center mt-6 space-x-2">
              {testimonials.map((_, index) => (
                <button
                  key={index}
                  className={`w-3 h-3 rounded-full transition-all duration-300 ${
                    index === currentTestimonial ? 'bg-cyan-400' : 'bg-gray-600'
                  }`}
                  onClick={() => setCurrentTestimonial(index)}
                />
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20 bg-gradient-to-r from-cyan-600 to-purple-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Stop Fraud Before It Happens?
          </h2>
          <p className="text-xl text-cyan-100 mb-8">
            Join thousands of security professionals using ScamShield AI to protect their organizations. 
            Start your free investigation today.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-white text-purple-600 hover:bg-gray-100 px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300 transform hover:scale-105 shadow-lg">
              Start Free Investigation
              <ArrowRight className="inline ml-2 h-5 w-5" />
            </button>
            <button className="border-2 border-white text-white hover:bg-white hover:text-purple-600 px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300">
              Schedule Demo
            </button>
          </div>

          <div className="mt-8 text-cyan-100">
            <p className="text-sm">
              ✓ 14-day free trial ✓ No credit card required ✓ Setup in 5 minutes
            </p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-slate-900 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center mb-4">
                <Shield className="h-8 w-8 text-cyan-400 mr-2" />
                <span className="text-xl font-bold text-white">ScamShield AI</span>
              </div>
              <p className="text-gray-400 mb-4">
                Elite AI-powered fraud investigation platform protecting millions worldwide.
              </p>
              <div className="flex space-x-4">
                <div className="w-8 h-8 bg-slate-700 rounded-full flex items-center justify-center">
                  <Globe className="h-4 w-4 text-gray-400" />
                </div>
                <div className="w-8 h-8 bg-slate-700 rounded-full flex items-center justify-center">
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

          <div className="border-t border-slate-700 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 ScamShield AI. All rights reserved. Born from a $500 scam, now protecting millions.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;

