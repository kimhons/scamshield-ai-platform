import React, { useState } from 'react';
import { 
  Check, 
  Shield, 
  Zap, 
  Brain, 
  Eye, 
  Users, 
  Star,
  Crown,
  Sparkles
} from 'lucide-react';

const PricingSection = () => {
  const [billingCycle, setBillingCycle] = useState('monthly');

  const pricingTiers = [
    {
      name: 'Free',
      badge: 'Beta',
      monthlyPrice: 0,
      annualPrice: 0,
      monthlyCredits: 3,
      description: 'Try our basic fraud detection',
      features: [
        '3 investigations per month',
        'Basic scam detection',
        'Community database access',
        'Email support',
        '1 concurrent investigation'
      ],
      buttonText: 'Get Started',
      buttonStyle: 'bg-gray-100 text-gray-800 hover:bg-gray-200',
      popular: false
    },
    {
      name: 'Basic',
      badge: 'Beta',
      monthlyPrice: 19.99,
      annualPrice: 16.59, // 17% discount
      monthlyCredits: 10,
      additionalCredits: 0.35,
      description: 'Perfect for individuals and small businesses',
      features: [
        '10 investigations per month',
        'Advanced AI analysis',
        'Multi-modal artifact support',
        'Priority email support',
        '2 concurrent investigations',
        'Basic reporting',
        'Mobile app access'
      ],
      buttonText: 'Upgrade to Basic',
      buttonStyle: 'bg-black text-white hover:bg-gray-800',
      popular: false
    },
    {
      name: 'Plus',
      badge: 'Beta',
      monthlyPrice: 89.99,
      annualPrice: 74.69, // 17% discount
      monthlyCredits: 25,
      additionalCredits: 1.85,
      description: 'Advanced AI for professional investigators',
      features: [
        '25 investigations per month',
        'Elite AI ensemble',
        'Behavioral profiling',
        'Intelligence fusion',
        '5 concurrent investigations',
        'Advanced reporting',
        'API access',
        'Team collaboration',
        'Custom alerts'
      ],
      buttonText: 'Upgrade to Plus',
      buttonStyle: 'bg-black text-white hover:bg-gray-800',
      popular: true
    },
    {
      name: 'Pro',
      badge: 'Beta',
      monthlyPrice: 399.99,
      annualPrice: 331.99, // 17% discount
      monthlyCredits: 100,
      additionalCredits: 7.25,
      description: 'Maximum capabilities for enterprises',
      features: [
        '100 investigations per month',
        'Maximum AI capabilities',
        'Strategic intelligence',
        'Threat attribution',
        '10 concurrent investigations',
        'White-label options',
        'Dedicated support',
        'Custom integrations',
        'SLA guarantees',
        'Executive briefings'
      ],
      buttonText: 'Upgrade to Pro',
      buttonStyle: 'bg-black text-white hover:bg-gray-800',
      popular: false
    }
  ];

  const getCurrentPrice = (tier) => {
    return billingCycle === 'monthly' ? tier.monthlyPrice : tier.annualPrice;
  };

  return (
    <div className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Choose Your Investigation Tier
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            From basic scam detection to elite intelligence analysis. 
            Professional-grade fraud investigation for every budget.
          </p>

          {/* Billing Toggle */}
          <div className="inline-flex items-center bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setBillingCycle('monthly')}
              className={`px-6 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                billingCycle === 'monthly'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setBillingCycle('annually')}
              className={`px-6 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                billingCycle === 'annually'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Annually
              <span className="ml-2 text-xs bg-blue-100 text-blue-600 px-2 py-1 rounded-full">
                Save 17%
              </span>
            </button>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {pricingTiers.map((tier, index) => (
            <div
              key={tier.name}
              className={`relative bg-white rounded-xl shadow-sm border transition-all duration-300 hover:shadow-lg ${
                tier.popular ? 'ring-2 ring-blue-500 shadow-blue-100' : 'border-gray-200'
              }`}
            >
              {tier.popular && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <span className="bg-blue-500 text-white px-4 py-1 rounded-full text-sm font-medium">
                    Most Popular
                  </span>
                </div>
              )}

              <div className="p-6">
                {/* Header */}
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-semibold text-gray-900">{tier.name}</h3>
                  <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full">
                    {tier.badge}
                  </span>
                </div>

                {/* Price */}
                <div className="mb-6">
                  <div className="flex items-baseline">
                    <span className="text-4xl font-bold text-gray-900">
                      ${getCurrentPrice(tier)}
                    </span>
                    <span className="text-gray-600 ml-1">/ month</span>
                  </div>
                  {billingCycle === 'annually' && tier.monthlyPrice > 0 && (
                    <div className="text-sm text-gray-500 mt-1">
                      ${tier.monthlyPrice}/month billed monthly
                    </div>
                  )}
                </div>

                {/* Action Button */}
                <button
                  className={`w-full py-3 px-4 rounded-lg font-medium text-sm transition-all duration-200 mb-6 ${tier.buttonStyle}`}
                  disabled={tier.name === 'Free'}
                >
                  {tier.name === 'Free' ? 'Current plan' : tier.buttonText}
                </button>

                {/* Credits Info */}
                {tier.monthlyCredits > 0 && (
                  <div className="mb-6 p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center text-sm text-gray-700 mb-1">
                      <Check className="h-4 w-4 text-green-500 mr-2" />
                      <span className="font-medium">{tier.monthlyCredits}</span>
                      <span className="ml-1">investigations per month</span>
                    </div>
                    {tier.additionalCredits && (
                      <div className="flex items-center text-sm text-gray-600">
                        <Zap className="h-4 w-4 text-blue-500 mr-2" />
                        <span>${tier.additionalCredits}</span>
                        <span className="ml-1">per additional investigation</span>
                      </div>
                    )}
                  </div>
                )}

                {/* Features */}
                <ul className="space-y-3">
                  {tier.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-start">
                      <Check className="h-4 w-4 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-sm text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom Sections */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Team Section */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center mb-4">
              <div className="bg-gray-100 rounded-lg p-2 mr-4">
                <Users className="h-6 w-6 text-gray-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Team</h3>
                <p className="text-sm text-gray-600">Scale your organization's fraud protection</p>
              </div>
            </div>
            <button className="bg-black text-white px-6 py-2 rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors">
              Contact Sales
            </button>
          </div>

          {/* Add-on Credits */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center mb-4">
              <div className="bg-blue-100 rounded-lg p-2 mr-4">
                <Sparkles className="h-6 w-6 text-blue-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Buy add-on investigations</h3>
                <p className="text-sm text-gray-600">One-time payment for additional investigations</p>
              </div>
            </div>
            <button className="bg-black text-white px-6 py-2 rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors">
              Buy investigations
            </button>
          </div>
        </div>

        {/* Additional Info */}
        <div className="text-center mt-12">
          <p className="text-gray-600 mb-4">
            All plans include 14-day free trial • No setup fees • Cancel anytime
          </p>
          <div className="flex justify-center items-center space-x-6 text-sm text-gray-500">
            <div className="flex items-center">
              <Shield className="h-4 w-4 mr-1" />
              Enterprise security
            </div>
            <div className="flex items-center">
              <Zap className="h-4 w-4 mr-1" />
              Real-time analysis
            </div>
            <div className="flex items-center">
              <Brain className="h-4 w-4 mr-1" />
              20+ AI models
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PricingSection;

