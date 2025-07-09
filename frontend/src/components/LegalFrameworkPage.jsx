import React, { useState } from 'react';
import { 
  Shield, Gavel, FileText, AlertTriangle, CheckCircle, Scale, 
  BookOpen, Award, Lock, UserCheck, Eye, ArrowRight, Download,
  ExternalLink, Info, AlertCircle, ShieldCheck
} from 'lucide-react';

const LegalFrameworkPage = () => {
  const [activeSection, setActiveSection] = useState('overview');

  const legalSections = [
    { id: 'overview', title: 'Legal Overview', icon: Scale },
    { id: 'terms', title: 'Terms of Service', icon: FileText },
    { id: 'ethics', title: 'Ethical Guidelines', icon: Award },
    { id: 'privacy', title: 'Privacy Policy', icon: Lock },
    { id: 'disclaimers', title: 'Disclaimers', icon: AlertTriangle },
    { id: 'compliance', title: 'Compliance Framework', icon: ShieldCheck }
  ];

  const legalProtections = [
    {
      title: "Limitation of Liability",
      description: "Comprehensive liability limitations protecting both platform and users from unintended consequences.",
      icon: Shield,
      details: [
        "Platform not liable for user decisions based on reports",
        "No warranties regarding accuracy or completeness",
        "Users assume responsibility for verification and actions",
        "Indemnification clauses protecting the platform"
      ]
    },
    {
      title: "Evidence-Based Methodology",
      description: "All analysis presents facts and evidence rather than definitive conclusions or accusations.",
      icon: Eye,
      details: [
        "No definitive accusations without overwhelming evidence",
        "All claims backed by verifiable sources",
        "Alternative explanations provided for findings",
        "Source reliability scoring and transparency"
      ]
    },
    {
      title: "User Responsibilities",
      description: "Clear requirements for users to independently verify information and use platform ethically.",
      icon: UserCheck,
      details: [
        "Independent verification required before action",
        "Professional consultation recommended for legal matters",
        "Ethical use requirements and guidelines",
        "Prohibition of harassment or defamatory use"
      ]
    },
    {
      title: "Professional Standards",
      description: "Industry-leading standards for fraud investigation with comprehensive quality assurance.",
      icon: Award,
      details: [
        "Evidence-based reporting methodology",
        "Multi-source verification requirements",
        "Quality assurance and expert review processes",
        "Continuous improvement and feedback integration"
      ]
    }
  ];

  const complianceFramework = [
    {
      category: "Data Protection",
      requirements: [
        "GDPR compliance for EU data subjects",
        "CCPA compliance for California residents",
        "Privacy by design principles",
        "Data minimization and purpose limitation"
      ],
      status: "Implemented"
    },
    {
      category: "Ethical AI",
      requirements: [
        "Bias mitigation in AI models",
        "Transparency in AI decision-making",
        "Human oversight for high-stakes decisions",
        "Continuous monitoring and improvement"
      ],
      status: "Enforced"
    },
    {
      category: "Professional Standards",
      requirements: [
        "Evidence-based methodology",
        "Source verification and reliability scoring",
        "Alternative explanation requirements",
        "Quality assurance processes"
      ],
      status: "Certified"
    },
    {
      category: "Legal Compliance",
      requirements: [
        "Comprehensive terms of service",
        "Liability limitation clauses",
        "User responsibility frameworks",
        "Dispute resolution mechanisms"
      ],
      status: "Validated"
    }
  ];

  const renderOverview = () => (
    <div className="space-y-8">
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
        <div className="flex items-start">
          <Info className="w-6 h-6 text-blue-600 mr-3 flex-shrink-0 mt-1" />
          <div>
            <h3 className="text-lg font-semibold text-blue-800 mb-2">Legal Framework Overview</h3>
            <p className="text-blue-700">
              ScamShield AI operates under a comprehensive legal framework designed to protect users, 
              investigated entities, and the platform itself. Our evidence-based methodology ensures 
              responsible and ethical fraud investigation.
            </p>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {legalProtections.map((protection, index) => (
          <div key={index} className="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-all duration-300">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                <protection.icon className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900">{protection.title}</h3>
            </div>
            <p className="text-gray-600 mb-4">{protection.description}</p>
            <ul className="space-y-2">
              {protection.details.map((detail, idx) => (
                <li key={idx} className="flex items-start text-sm text-gray-600">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                  {detail}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );

  const renderTermsOfService = () => (
    <div className="space-y-6">
      <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
        <div className="flex items-start">
          <AlertCircle className="w-6 h-6 text-yellow-600 mr-3 flex-shrink-0 mt-1" />
          <div>
            <h3 className="text-lg font-semibold text-yellow-800 mb-2">Important Legal Notice</h3>
            <p className="text-yellow-700">
              By using ScamShield AI, you agree to these terms and acknowledge that our service provides 
              evidence-based analysis for informational purposes only. You are responsible for independent 
              verification and all decisions based on our reports.
            </p>
          </div>
        </div>
      </div>

      <div className="prose max-w-none">
        <h3 className="text-2xl font-bold text-gray-900 mb-4">Terms of Service</h3>
        
        <div className="space-y-6">
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h4 className="text-lg font-semibold text-gray-900 mb-3">1. Nature of Service</h4>
            <p className="text-gray-600 mb-3">
              ScamShield AI provides automated analysis and information services for fraud detection and 
              investigation purposes. Our service is NOT a substitute for professional legal, financial, 
              or investigative advice.
            </p>
            <ul className="list-disc list-inside text-gray-600 space-y-1">
              <li>Evidence-based analysis using public information</li>
              <li>AI-powered pattern recognition and correlation</li>
              <li>Source verification and reliability scoring</li>
              <li>Professional reporting with legal disclaimers</li>
            </ul>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h4 className="text-lg font-semibold text-gray-900 mb-3">2. User Responsibilities</h4>
            <p className="text-gray-600 mb-3">
              Users agree to use our service responsibly and ethically, with full understanding of 
              the limitations and requirements for independent verification.
            </p>
            <ul className="list-disc list-inside text-gray-600 space-y-1">
              <li>Independent verification of all information before taking action</li>
              <li>Professional consultation for legal or financial matters</li>
              <li>Ethical use preventing harassment or defamation</li>
              <li>Compliance with all applicable laws and regulations</li>
            </ul>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h4 className="text-lg font-semibold text-gray-900 mb-3">3. Limitation of Liability</h4>
            <p className="text-gray-600 mb-3">
              ScamShield AI shall not be liable for any damages arising from your use of our service, 
              including but not limited to financial losses, reputational damage, or legal consequences.
            </p>
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mt-4">
              <p className="text-red-700 text-sm">
                <strong>Important:</strong> Users assume all responsibility for decisions and actions 
                taken based on our reports. We strongly recommend professional consultation for 
                significant decisions.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderEthicalGuidelines = () => (
    <div className="space-y-6">
      <div className="bg-green-50 border border-green-200 rounded-xl p-6">
        <div className="flex items-start">
          <Award className="w-6 h-6 text-green-600 mr-3 flex-shrink-0 mt-1" />
          <div>
            <h3 className="text-lg font-semibold text-green-800 mb-2">Ethical AI Leadership</h3>
            <p className="text-green-700">
              We are committed to the highest ethical standards in AI-powered fraud investigation, 
              prioritizing accuracy, fairness, transparency, and harm prevention in all our operations.
            </p>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <h3 className="text-xl font-bold text-gray-900">Core Ethical Principles</h3>
          
          <div className="space-y-4">
            {[
              {
                principle: "Accuracy",
                description: "All claims must be supported by verifiable evidence from reliable sources"
              },
              {
                principle: "Transparency", 
                description: "Sources and methodologies must be clearly disclosed and accessible"
              },
              {
                principle: "Fairness",
                description: "Analysis must be unbiased and consider alternative explanations"
              },
              {
                principle: "Responsibility",
                description: "Avoid making definitive accusations without overwhelming evidence"
              }
            ].map((item, index) => (
              <div key={index} className="bg-white border border-gray-200 rounded-lg p-4">
                <h4 className="font-semibold text-gray-900 mb-2">{item.principle}</h4>
                <p className="text-gray-600 text-sm">{item.description}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-4">
          <h3 className="text-xl font-bold text-gray-900">Prohibited Activities</h3>
          
          <div className="space-y-4">
            {[
              "Definitive criminal accusations without legal conviction",
              "Personal character assassinations or defamatory statements", 
              "Unverified financial claims or specific monetary damages",
              "Claims about protected characteristics (race, religion, etc.)",
              "Speculation about personal relationships or private matters",
              "Harassment, stalking, or intimidation behaviors"
            ].map((prohibition, index) => (
              <div key={index} className="bg-red-50 border border-red-200 rounded-lg p-3">
                <div className="flex items-start">
                  <AlertTriangle className="w-4 h-4 text-red-500 mr-2 flex-shrink-0 mt-0.5" />
                  <p className="text-red-700 text-sm">{prohibition}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const renderCompliance = () => (
    <div className="space-y-6">
      <div className="bg-purple-50 border border-purple-200 rounded-xl p-6">
        <div className="flex items-start">
          <ShieldCheck className="w-6 h-6 text-purple-600 mr-3 flex-shrink-0 mt-1" />
          <div>
            <h3 className="text-lg font-semibold text-purple-800 mb-2">Compliance Framework</h3>
            <p className="text-purple-700">
              Our comprehensive compliance framework ensures adherence to legal requirements, 
              ethical standards, and professional best practices across all jurisdictions.
            </p>
          </div>
        </div>
      </div>

      <div className="grid gap-6">
        {complianceFramework.map((framework, index) => (
          <div key={index} className="bg-white border border-gray-200 rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-gray-900">{framework.category}</h3>
              <span className="px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full">
                {framework.status}
              </span>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              {framework.requirements.map((requirement, idx) => (
                <div key={idx} className="flex items-start">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-600 text-sm">{requirement}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderContent = () => {
    switch (activeSection) {
      case 'overview': return renderOverview();
      case 'terms': return renderTermsOfService();
      case 'ethics': return renderEthicalGuidelines();
      case 'compliance': return renderCompliance();
      default: return renderOverview();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Shield className="w-8 h-8 text-blue-600 mr-3" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Legal Framework</h1>
                <p className="text-gray-600">Comprehensive legal protection and ethical guidelines</p>
              </div>
            </div>
            <div className="flex space-x-3">
              <button className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                <Download className="w-4 h-4 mr-2" />
                Download PDF
              </button>
              <button className="flex items-center px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                <ExternalLink className="w-4 h-4 mr-2" />
                Legal Contact
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar Navigation */}
          <div className="lg:w-1/4">
            <div className="bg-white rounded-xl border border-gray-200 p-6 sticky top-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Legal Sections</h3>
              <nav className="space-y-2">
                {legalSections.map((section) => (
                  <button
                    key={section.id}
                    onClick={() => setActiveSection(section.id)}
                    className={`w-full flex items-center px-3 py-2 rounded-lg text-left transition-colors ${
                      activeSection === section.id
                        ? 'bg-blue-100 text-blue-700 border border-blue-200'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <section.icon className="w-4 h-4 mr-3" />
                    {section.title}
                  </button>
                ))}
              </nav>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:w-3/4">
            <div className="bg-white rounded-xl border border-gray-200 p-8">
              {renderContent()}
            </div>
          </div>
        </div>
      </div>

      {/* Footer CTA */}
      <div className="bg-gray-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Questions About Our Legal Framework?</h2>
          <p className="text-gray-300 mb-8 max-w-2xl mx-auto">
            Our legal team is available to answer questions about our compliance framework, 
            ethical guidelines, and professional standards.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
              Contact Legal Team
              <ArrowRight className="inline ml-2 w-5 h-5" />
            </button>
            <button className="border border-gray-300 text-gray-300 px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-gray-900 transition-colors">
              Schedule Consultation
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LegalFrameworkPage;

