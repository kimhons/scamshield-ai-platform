import React, { useState } from 'react';
import { Check, Zap, Shield, Crown, Building, Sparkles } from 'lucide-react';

const CreditPricingSection = () => {
  const [isAnnual, setIsAnnual] = useState(false);

  const plans = [
    {
      name: "Free",
      badge: "Beta",
      price: isAnnual ? 0 : 0,
      credits: "100 credits",
      description: "Basic fraud detection",
      buttonText: "Current plan",
      buttonStyle: "bg-gray-400 text-white cursor-not-allowed",
      popular: false,
      features: [
        "100 credits per month",
        "Basic scam detection",
        "Community database access", 
        "Email support",
        "1 concurrent investigation",
        "Basic text reports",
        "URL analysis",
        "Simple risk scoring"
      ]
    },
    {
      name: "Basic",
      badge: "Beta", 
      price: isAnnual ? 199.90 : 19.99,
      credits: "1,900 credits",
      description: "Advanced AI analysis",
      buttonText: "Upgrade to Basic",
      buttonStyle: "bg-black text-white hover:bg-gray-800",
      popular: false,
      features: [
        "1,900 credits per month",
        "Multi-modal analysis (URLs, emails, images)",
        "Advanced AI models (GPT-4o-mini, Claude Haiku)",
        "Priority email support (24-48h response)",
        "2 concurrent investigations", 
        "Standard reports with visualizations",
        "20% credit rollover",
        "Mobile app access",
        "Basic behavioral analysis"
      ]
    },
    {
      name: "Plus",
      badge: "Beta",
      price: isAnnual ? 899.90 : 89.99,
      credits: "9,500 credits", 
      description: "Elite AI ensemble + behavioral profiling",
      buttonText: "Upgrade to Plus",
      buttonStyle: "bg-black text-white hover:bg-gray-800",
      popular: true,
      features: [
        "9,500 credits per month",
        "Advanced behavioral profiling",
        "Intelligence fusion & threat correlation",
        "API access for integrations",
        "5 concurrent investigations",
        "Advanced reports with interactive visualizations",
        "Priority processing (1.5x speed)",
        "Phone support",
        "Custom alerts & notifications",
        "Document forensic analysis",
        "Social media investigation",
        "Cryptocurrency address analysis"
      ]
    },
    {
      name: "Pro", 
      badge: "Beta",
      price: isAnnual ? 3999.90 : 399.99,
      credits: "45,000 credits",
      description: "Maximum AI capabilities + threat attribution",
      buttonText: "Upgrade to Pro",
      buttonStyle: "bg-black text-white hover:bg-gray-800",
      popular: false,
      features: [
        "45,000 credits per month",
        "Elite AI ensemble (20+ models)",
        "Threat attribution analysis",
        "Predictive modeling & forecasting",
        "White-label reports with custom branding",
        "10 concurrent investigations",
        "Executive reports with strategic intelligence",
        "Emergency processing (2x speed)",
        "Dedicated support manager",
        "SLA guarantees (99.9% uptime)",
        "Custom integrations (SIEM, security tools)",
        "Advanced network analysis",
        "Threat actor profiling",
        "Campaign attribution",
        "Real-time threat intelligence feeds"
      ]
    }
  ];

  const creditUsageExamples = [
    { type: "Basic URL scan", credits: "10-30 credits", icon: Zap },
    { type: "Email investigation", credits: "40-120 credits", icon: Shield },
    { type: "Image analysis", credits: "60-180 credits", icon: Sparkles },
    { type: "Elite investigation", credits: "800-2000 credits", icon: Crown }
  ];

  return (
    <div className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Choose Your Investigation Tier
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Dynamic credit system - pay based on computational load and AI models used
          </p>
          
          {/* Toggle */}
          <div className="flex items-center justify-center mb-8">
            <span className={`mr-3 ${!isAnnual ? 'text-gray-900 font-medium' : 'text-gray-500'}`}>
              Monthly
            </span>
            <button
              onClick={() => setIsAnnual(!isAnnual)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                isAnnual ? 'bg-blue-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  isAnnual ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
            <span className={`ml-3 ${isAnnual ? 'text-gray-900 font-medium' : 'text-gray-500'}`}>
              Annually
            </span>
            {isAnnual && (
              <span className="ml-2 text-sm text-blue-600 font-medium">Save 17%</span>
            )}
          </div>
        </div>

        {/* Credit Usage Examples */}
        <div className="mb-16">
          <h3 className="text-2xl font-bold text-center text-gray-900 mb-8">
            Credit Usage Examples
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {creditUsageExamples.map((example, index) => (
              <div key={index} className="bg-white rounded-lg p-6 text-center border border-gray-200">
                <div className="bg-blue-100 rounded-lg p-3 w-fit mx-auto mb-4">
                  <example.icon className="h-6 w-6 text-blue-600" />
                </div>
                <h4 className="font-semibold text-gray-900 mb-2">{example.type}</h4>
                <p className="text-blue-600 font-medium">{example.credits}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {plans.map((plan, index) => (
            <div
              key={index}
              className={`relative bg-white rounded-xl border-2 p-8 ${
                plan.popular 
                  ? 'border-blue-500 shadow-lg scale-105' 
                  : 'border-gray-200 shadow-sm'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-blue-500 text-white px-4 py-1 rounded-full text-sm font-medium">
                    Most Popular
                  </span>
                </div>
              )}

              <div className="text-center">
                <div className="flex items-center justify-center gap-2 mb-4">
                  <h3 className="text-xl font-bold text-gray-900">{plan.name}</h3>
                  <span className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs font-medium">
                    {plan.badge}
                  </span>
                </div>

                <div className="mb-4">
                  <span className="text-4xl font-bold text-gray-900">
                    ${plan.price}
                  </span>
                  <span className="text-gray-600">/ month</span>
                </div>

                <div className="mb-6">
                  <div className="text-lg font-semibold text-blue-600">
                    {plan.credits}
                  </div>
                </div>

                <button className={`w-full py-3 px-4 rounded-lg font-medium transition-all duration-200 mb-6 ${plan.buttonStyle}`}>
                  {plan.buttonText}
                </button>

                <div className="text-left">
                  <ul className="space-y-3">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-start">
                        <Check className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                        <span className="text-gray-700 text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Additional Options */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white rounded-xl p-8 border border-gray-200">
            <div className="flex items-center mb-4">
              <Building className="h-8 w-8 text-blue-600 mr-3" />
              <h3 className="text-xl font-bold text-gray-900">Enterprise</h3>
            </div>
            <p className="text-gray-600 mb-6">
              Custom solutions for large organizations with unlimited credits and advanced features.
            </p>
            <button className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors">
              Contact Sales
            </button>
          </div>

          <div className="bg-white rounded-xl p-8 border border-gray-200">
            <div className="flex items-center mb-4">
              <Sparkles className="h-8 w-8 text-purple-600 mr-3" />
              <h3 className="text-xl font-bold text-gray-900">Buy Additional Credits</h3>
            </div>
            <p className="text-gray-600 mb-6">
              Need more credits? Purchase additional credit packs at discounted rates.
            </p>
            <button className="bg-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-purple-700 transition-colors">
              Buy Credits
            </button>
          </div>
        </div>

        {/* Features Note */}
        <div className="mt-12 text-center">
          <p className="text-gray-600">
            All plans include 14-day free trial • No setup fees • Cancel anytime
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Credits are consumed based on computational load and AI models used • 20% unused credits roll over (max 1 month)
          </p>
        </div>
      </div>
    </div>
  );
};

export default CreditPricingSection;

