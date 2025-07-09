import React, { useState } from 'react';
import { 
  Check, Zap, Shield, Crown, Building, Sparkles, Scale, Award, 
  ShieldCheck, FileText, Eye, Brain, Database, Lock, Users,
  Star, ArrowRight, AlertCircle, CheckCircle
} from 'lucide-react';

const EnhancedCreditPricingSection = () => {
  const [isAnnual, setIsAnnual] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState('plus');

  const plans = [
    {
      id: "free",
      name: "Free",
      badge: "Community",
      badgeColor: "bg-gray-100 text-gray-800",
      price: 0,
      credits: "500 credits",
      description: "Basic evidence-based analysis",
      buttonText: "Start Free",
      buttonStyle: "bg-gray-600 text-white hover:bg-gray-700",
      popular: false,
      icon: Shield,
      features: [
        "500 credits per month",
        "Basic evidence-based analysis",
        "Community database access", 
        "Email support (72h response)",
        "1 concurrent investigation",
        "Basic text reports with disclaimers",
        "URL and domain analysis",
        "Simple risk indicators",
        "Source transparency",
        "Legal compliance framework"
      ],
      limitations: [
        "Limited AI models",
        "Basic verification only",
        "No expert review"
      ],
      ethicalFeatures: [
        "Evidence-based methodology",
        "Legal disclaimers included",
        "Source transparency"
      ]
    },
    {
      id: "basic",
      name: "Basic",
      badge: "Professional", 
      badgeColor: "bg-blue-100 text-blue-800",
      price: isAnnual ? 199.90 : 19.99,
      credits: "1,900 credits",
      description: "Professional fraud investigation",
      buttonText: "Upgrade to Basic",
      buttonStyle: "bg-blue-600 text-white hover:bg-blue-700",
      popular: false,
      icon: Eye,
      features: [
        "1,900 credits per month",
        "Multi-modal analysis (URLs, emails, images)",
        "Advanced AI models (GPT-4o-mini, Claude Haiku)",
        "Priority email support (24-48h response)",
        "2 concurrent investigations", 
        "Professional reports with evidence citations",
        "20% credit rollover",
        "Mobile app access",
        "Behavioral pattern analysis",
        "50+ public API integrations",
        "Evidence reliability scoring",
        "Alternative explanations provided"
      ],
      limitations: [
        "Standard AI models only",
        "Automated quality checks",
        "Limited concurrent investigations"
      ],
      ethicalFeatures: [
        "Evidence-based reporting",
        "Source reliability scoring",
        "Professional disclaimers",
        "Ethical use guidelines"
      ]
    },
    {
      id: "plus",
      name: "Plus",
      badge: "Most Popular",
      badgeColor: "bg-purple-100 text-purple-800",
      price: isAnnual ? 949.90 : 94.99,
      credits: "9,500 credits",
      description: "Advanced investigation with expert features",
      buttonText: "Upgrade to Plus",
      buttonStyle: "bg-purple-600 text-white hover:bg-purple-700",
      popular: true,
      icon: Brain,
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
        "Cryptocurrency address analysis",
        "Expert quality assurance",
        "Comprehensive evidence packages"
      ],
      limitations: [
        "Advanced AI models",
        "Human quality checks",
        "Professional consultation available"
      ],
      ethicalFeatures: [
        "Multi-source verification",
        "Expert evidence review",
        "Comprehensive legal protection",
        "Professional standards compliance"
      ]
    },
    {
      id: "pro",
      name: "Pro",
      badge: "Elite",
      badgeColor: "bg-orange-100 text-orange-800",
      price: isAnnual ? 4499.90 : 449.99,
      credits: "45,000 credits",
      description: "Elite investigation with human expert review",
      buttonText: "Upgrade to Pro",
      buttonStyle: "bg-orange-600 text-white hover:bg-orange-700",
      popular: false,
      icon: Crown,
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
        "Human expert review for all reports",
        "Legal consultation included"
      ],
      limitations: [],
      ethicalFeatures: [
        "Human expert validation",
        "Legal consultation included",
        "Custom compliance frameworks",
        "Professional liability coverage"
      ]
    },
    {
      id: "enterprise",
      name: "Enterprise",
      badge: "Custom",
      badgeColor: "bg-green-100 text-green-800",
      price: "Custom",
      credits: "Unlimited",
      description: "Custom solutions with dedicated support",
      buttonText: "Contact Sales",
      buttonStyle: "bg-green-600 text-white hover:bg-green-700",
      popular: false,
      icon: Building,
      features: [
        "Unlimited credits",
        "Custom AI model training",
        "Dedicated infrastructure",
        "White-label platform",
        "Custom integrations",
        "Dedicated account manager",
        "24/7 priority support",
        "Custom SLA agreements",
        "On-premise deployment options",
        "Custom compliance frameworks",
        "Advanced security features",
        "Custom reporting templates",
        "Professional services included",
        "Legal team consultation",
        "Regulatory compliance assistance"
      ],
      limitations: [],
      ethicalFeatures: [
        "Custom ethical frameworks",
        "Dedicated legal support",
        "Regulatory compliance assistance",
        "Professional liability coverage"
      ]
    }
  ];

  const ethicalHighlights = [
    {
      icon: Scale,
      title: "Evidence-Based Analysis",
      description: "All findings backed by verifiable sources with reliability scoring"
    },
    {
      icon: ShieldCheck,
      title: "Legal Compliance",
      description: "Comprehensive legal framework protecting all parties"
    },
    {
      icon: Award,
      title: "Professional Standards",
      description: "Industry-leading ethical standards and quality assurance"
    },
    {
      icon: Lock,
      title: "Privacy Protection",
      description: "Robust privacy safeguards and confidentiality measures"
    }
  ];

  const comparisonFeatures = [
    {
      category: "Investigation Capabilities",
      features: [
        { name: "Evidence-based analysis", free: true, basic: true, plus: true, pro: true, enterprise: true },
        { name: "Multi-modal analysis", free: false, basic: true, plus: true, pro: true, enterprise: true },
        { name: "Advanced AI models", free: false, basic: "Limited", plus: true, pro: "Elite", enterprise: "Custom" },
        { name: "Concurrent investigations", free: "1", basic: "2", plus: "5", pro: "10", enterprise: "Unlimited" },
        { name: "Processing speed", free: "Standard", basic: "Standard", plus: "1.5x", pro: "2x", enterprise: "Custom" }
      ]
    },
    {
      category: "Ethical & Legal Features",
      features: [
        { name: "Legal disclaimers", free: true, basic: true, plus: true, pro: true, enterprise: true },
        { name: "Source transparency", free: true, basic: true, plus: true, pro: true, enterprise: true },
        { name: "Evidence reliability scoring", free: false, basic: true, plus: true, pro: true, enterprise: true },
        { name: "Alternative explanations", free: false, basic: true, plus: true, pro: true, enterprise: true },
        { name: "Expert review", free: false, basic: false, plus: "Quality checks", pro: "Full review", enterprise: "Custom" }
      ]
    },
    {
      category: "Support & Compliance",
      features: [
        { name: "Email support", free: "72h", basic: "24-48h", plus: "Priority", pro: "Dedicated", enterprise: "24/7" },
        { name: "Legal consultation", free: false, basic: false, plus: false, pro: true, enterprise: true },
        { name: "Compliance assistance", free: false, basic: false, plus: false, pro: false, enterprise: true },
        { name: "Professional liability", free: false, basic: false, plus: false, pro: true, enterprise: true }
      ]
    }
  ];

  return (
    <div className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-blue-100 text-blue-800 text-sm font-medium mb-4">
            <Scale className="w-4 h-4 mr-2" />
            Ethical AI • Evidence-Based • Legally Compliant
          </div>
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Professional Fraud Investigation Pricing
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            Choose the plan that fits your investigation needs. All plans include our ethical framework, 
            evidence-based methodology, and comprehensive legal protection.
          </p>
          
          {/* Billing Toggle */}
          <div className="flex items-center justify-center mb-8">
            <span className={`mr-3 ${!isAnnual ? 'text-gray-900 font-medium' : 'text-gray-500'}`}>
              Monthly
            </span>
            <button
              onClick={() => setIsAnnual(!isAnnual)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
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
              Annual
            </span>
            {isAnnual && (
              <span className="ml-2 px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                Save 20%
              </span>
            )}
          </div>
        </div>

        {/* Ethical Highlights */}
        <div className="grid md:grid-cols-4 gap-6 mb-16">
          {ethicalHighlights.map((highlight, index) => (
            <div key={index} className="bg-white rounded-xl border border-gray-200 p-6 text-center hover:shadow-lg transition-all duration-300">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <highlight.icon className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{highlight.title}</h3>
              <p className="text-gray-600 text-sm">{highlight.description}</p>
            </div>
          ))}
        </div>

        {/* Pricing Cards */}
        <div className="grid lg:grid-cols-5 gap-6 mb-16">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className={`relative bg-white rounded-2xl border-2 p-8 hover:shadow-xl transition-all duration-300 ${
                plan.popular 
                  ? 'border-purple-500 shadow-lg transform scale-105' 
                  : 'border-gray-200 hover:border-blue-300'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-purple-600 text-white px-4 py-2 rounded-full text-sm font-medium">
                    Most Popular
                  </span>
                </div>
              )}
              
              <div className="text-center mb-6">
                <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <plan.icon className="w-6 h-6 text-gray-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${plan.badgeColor}`}>
                  {plan.badge}
                </span>
              </div>
              
              <div className="text-center mb-6">
                <div className="text-4xl font-bold text-gray-900 mb-2">
                  {typeof plan.price === 'number' ? (
                    <>
                      ${plan.price}
                      <span className="text-lg text-gray-500 font-normal">
                        /{isAnnual ? 'year' : 'month'}
                      </span>
                    </>
                  ) : (
                    plan.price
                  )}
                </div>
                <div className="text-lg text-blue-600 font-semibold">{plan.credits}</div>
                <p className="text-gray-600 text-sm mt-2">{plan.description}</p>
              </div>
              
              <button className={`w-full py-3 px-4 rounded-lg font-semibold transition-all duration-300 mb-6 ${plan.buttonStyle}`}>
                {plan.buttonText}
              </button>
              
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-gray-900 mb-3">Features</h4>
                  <ul className="space-y-2">
                    {plan.features.slice(0, 6).map((feature, index) => (
                      <li key={index} className="flex items-start text-sm text-gray-600">
                        <CheckCircle className="w-4 h-4 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                        {feature}
                      </li>
                    ))}
                    {plan.features.length > 6 && (
                      <li className="text-sm text-blue-600 font-medium">
                        +{plan.features.length - 6} more features
                      </li>
                    )}
                  </ul>
                </div>
                
                <div>
                  <h4 className="font-semibold text-gray-900 mb-3">Ethical Features</h4>
                  <ul className="space-y-2">
                    {plan.ethicalFeatures.map((feature, index) => (
                      <li key={index} className="flex items-start text-sm text-green-700">
                        <Scale className="w-4 h-4 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Feature Comparison Table */}
        <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden mb-16">
          <div className="px-8 py-6 bg-gray-50 border-b border-gray-200">
            <h3 className="text-2xl font-bold text-gray-900">Detailed Feature Comparison</h3>
            <p className="text-gray-600 mt-2">Compare all features across our professional investigation plans</p>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-4 px-6 font-semibold text-gray-900">Features</th>
                  <th className="text-center py-4 px-4 font-semibold text-gray-900">Free</th>
                  <th className="text-center py-4 px-4 font-semibold text-gray-900">Basic</th>
                  <th className="text-center py-4 px-4 font-semibold text-gray-900 bg-purple-50">Plus</th>
                  <th className="text-center py-4 px-4 font-semibold text-gray-900">Pro</th>
                  <th className="text-center py-4 px-4 font-semibold text-gray-900">Enterprise</th>
                </tr>
              </thead>
              <tbody>
                {comparisonFeatures.map((category, categoryIndex) => (
                  <React.Fragment key={categoryIndex}>
                    <tr className="bg-gray-50">
                      <td colSpan={6} className="py-3 px-6 font-semibold text-gray-900 text-sm uppercase tracking-wide">
                        {category.category}
                      </td>
                    </tr>
                    {category.features.map((feature, featureIndex) => (
                      <tr key={featureIndex} className="border-b border-gray-100 hover:bg-gray-50">
                        <td className="py-3 px-6 text-gray-700">{feature.name}</td>
                        <td className="py-3 px-4 text-center">
                          {typeof feature.free === 'boolean' ? (
                            feature.free ? (
                              <CheckCircle className="w-5 h-5 text-green-500 mx-auto" />
                            ) : (
                              <span className="text-gray-400">—</span>
                            )
                          ) : (
                            <span className="text-sm text-gray-600">{feature.free}</span>
                          )}
                        </td>
                        <td className="py-3 px-4 text-center">
                          {typeof feature.basic === 'boolean' ? (
                            feature.basic ? (
                              <CheckCircle className="w-5 h-5 text-green-500 mx-auto" />
                            ) : (
                              <span className="text-gray-400">—</span>
                            )
                          ) : (
                            <span className="text-sm text-gray-600">{feature.basic}</span>
                          )}
                        </td>
                        <td className="py-3 px-4 text-center bg-purple-50">
                          {typeof feature.plus === 'boolean' ? (
                            feature.plus ? (
                              <CheckCircle className="w-5 h-5 text-green-500 mx-auto" />
                            ) : (
                              <span className="text-gray-400">—</span>
                            )
                          ) : (
                            <span className="text-sm text-gray-600 font-medium">{feature.plus}</span>
                          )}
                        </td>
                        <td className="py-3 px-4 text-center">
                          {typeof feature.pro === 'boolean' ? (
                            feature.pro ? (
                              <CheckCircle className="w-5 h-5 text-green-500 mx-auto" />
                            ) : (
                              <span className="text-gray-400">—</span>
                            )
                          ) : (
                            <span className="text-sm text-gray-600">{feature.pro}</span>
                          )}
                        </td>
                        <td className="py-3 px-4 text-center">
                          {typeof feature.enterprise === 'boolean' ? (
                            feature.enterprise ? (
                              <CheckCircle className="w-5 h-5 text-green-500 mx-auto" />
                            ) : (
                              <span className="text-gray-400">—</span>
                            )
                          ) : (
                            <span className="text-sm text-gray-600">{feature.enterprise}</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Legal Notice */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6 mb-16">
          <div className="flex items-start">
            <AlertCircle className="w-6 h-6 text-yellow-600 mr-3 flex-shrink-0 mt-1" />
            <div>
              <h3 className="text-lg font-semibold text-yellow-800 mb-2">Important Legal Notice</h3>
              <p className="text-yellow-700 mb-4">
                All ScamShield AI plans include comprehensive legal protection and ethical compliance. 
                Our service provides evidence-based analysis for informational purposes only. 
                Users are responsible for independent verification and all decisions based on our reports.
              </p>
              <div className="flex flex-wrap gap-4">
                <button className="text-yellow-800 hover:text-yellow-900 font-medium text-sm underline">
                  View Legal Framework
                </button>
                <button className="text-yellow-800 hover:text-yellow-900 font-medium text-sm underline">
                  Ethical Guidelines
                </button>
                <button className="text-yellow-800 hover:text-yellow-900 font-medium text-sm underline">
                  Terms of Service
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="text-center">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            Questions About Our Pricing?
          </h3>
          <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
            Our team is here to help you choose the right plan for your fraud investigation needs 
            and answer any questions about our ethical framework and legal compliance.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
              Contact Sales Team
              <ArrowRight className="inline ml-2 w-5 h-5" />
            </button>
            <button className="border border-gray-300 text-gray-700 px-8 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors">
              Schedule Demo
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedCreditPricingSection;

