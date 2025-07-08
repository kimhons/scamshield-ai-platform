import React, { useState, useEffect } from 'react';
import { 
  AlertTriangle, 
  TrendingUp, 
  Users, 
  DollarSign, 
  Shield, 
  Zap, 
  Brain, 
  CheckCircle,
  ArrowRight,
  Target,
  Clock,
  Globe,
  Phone,
  Mail,
  CreditCard,
  Building,
  Home
} from 'lucide-react';

const ProblemSolutionSection = () => {
  const [currentStat, setCurrentStat] = useState(0);

  const fraudStats = [
    {
      number: "$5.8 Trillion",
      label: "Global fraud losses in 2024",
      icon: DollarSign,
      color: "text-red-600",
      bgColor: "bg-red-100"
    },
    {
      number: "2.8 Billion",
      label: "People targeted by scams annually",
      icon: Users,
      color: "text-orange-600",
      bgColor: "bg-orange-100"
    },
    {
      number: "300%",
      label: "Increase in AI-powered scams",
      icon: TrendingUp,
      color: "text-red-600",
      bgColor: "bg-red-100"
    },
    {
      number: "15 Minutes",
      label: "Average time to lose money to scams",
      icon: Clock,
      color: "text-yellow-600",
      bgColor: "bg-yellow-100"
    }
  ];

  const scamTypes = [
    {
      icon: Phone,
      title: "Phone & SMS Scams",
      victims: "1.2B people targeted",
      loss: "$39.5B lost annually",
      description: "Robocalls, fake tech support, phishing SMS"
    },
    {
      icon: Mail,
      title: "Email & Phishing",
      victims: "3.4B emails sent daily",
      loss: "$12.5B lost annually", 
      description: "Business email compromise, fake invoices, credential theft"
    },
    {
      icon: CreditCard,
      title: "Financial Fraud",
      victims: "127M people affected",
      loss: "$56B lost annually",
      description: "Credit card fraud, investment scams, crypto theft"
    },
    {
      icon: Building,
      title: "Business Scams",
      victims: "43% of businesses targeted",
      loss: "$2.9B lost annually",
      description: "Vendor fraud, fake suppliers, invoice manipulation"
    },
    {
      icon: Home,
      title: "Romance & Social",
      victims: "70M people vulnerable",
      loss: "$1.3B lost annually",
      description: "Dating scams, social media fraud, fake relationships"
    },
    {
      icon: Globe,
      title: "Online Shopping",
      victims: "230M shoppers affected",
      loss: "$8.2B lost annually",
      description: "Fake websites, counterfeit goods, payment fraud"
    }
  ];

  const solutions = [
    {
      icon: Brain,
      title: "AI-Powered Detection",
      problem: "Traditional methods miss 67% of new scams",
      solution: "Our 20+ AI models detect 99.9% of fraud patterns",
      improvement: "3x better detection rate"
    },
    {
      icon: Zap,
      title: "Real-Time Analysis",
      problem: "Manual investigation takes 2-4 weeks",
      solution: "Instant analysis in 15 seconds average",
      improvement: "672x faster processing"
    },
    {
      icon: Target,
      title: "Multi-Modal Intelligence",
      problem: "Single-point analysis misses complex schemes",
      solution: "Analyze URLs, emails, images, documents, phone numbers simultaneously",
      improvement: "Complete threat visibility"
    },
    {
      icon: Shield,
      title: "Proactive Protection",
      problem: "Reactive approach - damage already done",
      solution: "Predict and prevent fraud before money is lost",
      improvement: "Prevention vs. recovery"
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStat((prev) => (prev + 1) % fraudStats.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="py-20 bg-gradient-to-br from-red-50 to-orange-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Crisis Header */}
        <div className="text-center mb-16">
          <div className="flex justify-center mb-6">
            <div className="bg-red-100 rounded-full p-4">
              <AlertTriangle className="h-12 w-12 text-red-600" />
            </div>
          </div>
          
          <h2 className="text-5xl font-bold text-gray-900 mb-6">
            The <span className="text-red-600">Fraud Crisis</span> is Out of Control
          </h2>
          
          <p className="text-xl text-gray-700 max-w-4xl mx-auto mb-8">
            Every day, millions of people and businesses lose money to increasingly sophisticated scams. 
            Traditional security measures are failing against AI-powered fraud.
          </p>

          {/* Rotating Stats */}
          <div className="bg-white rounded-xl p-8 shadow-lg border-2 border-red-200 max-w-md mx-auto">
            <div className={`${fraudStats[currentStat].bgColor} rounded-lg p-4 mb-4 mx-auto w-fit`}>
              {React.createElement(fraudStats[currentStat].icon, { 
                className: `h-8 w-8 ${fraudStats[currentStat].color}` 
              })}
            </div>
            <div className={`text-4xl font-bold ${fraudStats[currentStat].color} mb-2`}>
              {fraudStats[currentStat].number}
            </div>
            <div className="text-gray-700 font-medium">
              {fraudStats[currentStat].label}
            </div>
          </div>
        </div>

        {/* Scam Types Grid */}
        <div className="mb-20">
          <h3 className="text-3xl font-bold text-center text-gray-900 mb-12">
            The Scale of the Problem
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {scamTypes.map((scam, index) => (
              <div key={index} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-lg transition-all duration-300">
                <div className="bg-red-100 rounded-lg p-3 w-fit mb-4">
                  <scam.icon className="h-6 w-6 text-red-600" />
                </div>
                <h4 className="text-lg font-bold text-gray-900 mb-2">{scam.title}</h4>
                <div className="space-y-1 mb-3">
                  <div className="text-red-600 font-semibold text-sm">{scam.victims}</div>
                  <div className="text-red-700 font-bold">{scam.loss}</div>
                </div>
                <p className="text-gray-600 text-sm">{scam.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Solution Section */}
        <div className="bg-white rounded-2xl p-8 shadow-xl border border-gray-200">
          <div className="text-center mb-12">
            <div className="flex justify-center mb-6">
              <div className="bg-blue-100 rounded-full p-4">
                <Shield className="h-12 w-12 text-blue-600" />
              </div>
            </div>
            
            <h3 className="text-4xl font-bold text-gray-900 mb-4">
              How <span className="text-blue-600">ScamShield AI</span> Solves This Crisis
            </h3>
            
            <p className="text-xl text-gray-700 max-w-3xl mx-auto">
              Born from a real $500 scam experience, we've built the world's most advanced 
              AI-powered fraud prevention platform to protect millions.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {solutions.map((solution, index) => (
              <div key={index} className="bg-gray-50 rounded-xl p-6 border border-gray-200">
                <div className="flex items-start space-x-4">
                  <div className="bg-blue-100 rounded-lg p-3 flex-shrink-0">
                    <solution.icon className="h-6 w-6 text-blue-600" />
                  </div>
                  
                  <div className="flex-1">
                    <h4 className="text-xl font-bold text-gray-900 mb-3">{solution.title}</h4>
                    
                    <div className="space-y-3">
                      <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                        <div className="flex items-center text-red-700 text-sm font-medium mb-1">
                          <AlertTriangle className="h-4 w-4 mr-2" />
                          Problem
                        </div>
                        <p className="text-red-800 text-sm">{solution.problem}</p>
                      </div>
                      
                      <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                        <div className="flex items-center text-green-700 text-sm font-medium mb-1">
                          <CheckCircle className="h-4 w-4 mr-2" />
                          Our Solution
                        </div>
                        <p className="text-green-800 text-sm">{solution.solution}</p>
                      </div>
                      
                      <div className="bg-blue-50 border border-blue-200 rounded-lg p-2">
                        <div className="text-blue-700 font-bold text-sm text-center">
                          ⚡ {solution.improvement}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Technical Capabilities */}
          <div className="mt-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-8 text-white text-center">
            <h4 className="text-2xl font-bold mb-6">Our Technical Capabilities</h4>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div>
                <div className="text-3xl font-bold mb-2">20+</div>
                <div className="text-blue-100">AI Models</div>
              </div>
              <div>
                <div className="text-3xl font-bold mb-2">Multi-Modal</div>
                <div className="text-blue-100">Analysis</div>
              </div>
              <div>
                <div className="text-3xl font-bold mb-2">Real-Time</div>
                <div className="text-blue-100">Processing</div>
              </div>
              <div>
                <div className="text-3xl font-bold mb-2">Enterprise</div>
                <div className="text-blue-100">Security</div>
              </div>
            </div>
            
            <div className="mt-8">
              <button className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300 transform hover:scale-105 shadow-lg">
                Start Your Free Investigation
                <ArrowRight className="inline ml-2 h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProblemSolutionSection;

