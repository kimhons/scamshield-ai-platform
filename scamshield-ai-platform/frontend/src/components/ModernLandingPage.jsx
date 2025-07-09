import React, { useState, useEffect, useRef } from 'react';
import { motion, useScroll, useTransform, useInView } from 'framer-motion';
import { 
  Shield, Brain, Zap, Users, CheckCircle, ArrowRight, Star, Globe, TrendingUp, 
  AlertTriangle, Eye, Target, Cpu, Database, Lock, Scale, FileText, 
  Award, Search, Clock, DollarSign, BarChart3, Microscope, ShieldCheck,
  Sparkles, Play, Rocket, ChevronDown, Menu, X, 
  Bot, Network, Fingerprint, Radar, MessageSquare, AlertCircle,
  TrendingDown, Activity, Layers, MousePointer, Smartphone
} from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';

// Hero section with premium animations
const HeroSection = () => {
  const [isVisible, setIsVisible] = useState(false);
  const heroRef = useRef(null);
  const { scrollY } = useScroll();
  const y = useTransform(scrollY, [0, 500], [0, 150]);
  const opacity = useTransform(scrollY, [0, 300], [1, 0]);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  return (
    <section ref={heroRef} className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-background via-muted/20 to-background">
        <div className="absolute inset-0 bg-noise opacity-30"></div>
        <motion.div 
          className="absolute top-20 left-20 w-72 h-72 bg-primary/20 rounded-full blur-3xl"
          animate={{ scale: [1, 1.2, 1], rotate: [0, 180, 360] }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        />
        <motion.div 
          className="absolute bottom-20 right-20 w-96 h-96 bg-accent/20 rounded-full blur-3xl"
          animate={{ scale: [1.2, 1, 1.2], rotate: [360, 180, 0] }}
          transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
        />
      </div>

      <motion.div 
        style={{ y, opacity }}
        className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center"
      >
        {/* Premium Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: isVisible ? 1 : 0, y: isVisible ? 0 : 20 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mb-8"
        >
          <Badge className="bg-gradient-premium text-white px-6 py-2 text-sm font-medium rounded-full shadow-glow">
            <Sparkles className="w-4 h-4 mr-2" />
            Next-Generation AI Security Platform
          </Badge>
        </motion.div>

        {/* Main Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: isVisible ? 1 : 0, y: isVisible ? 0 : 30 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="text-5xl md:text-7xl lg:text-8xl font-bold mb-6 leading-tight"
        >
          <span className="gradient-text font-tech">ScamShield</span>
          <br />
          <span className="text-foreground">AI Protection</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: isVisible ? 1 : 0, y: isVisible ? 0 : 20 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-3xl mx-auto leading-relaxed"
        >
          Leverage advanced AI to detect, investigate, and prevent sophisticated scams and fraud. 
          Protect your digital assets with enterprise-grade intelligence.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: isVisible ? 1 : 0, y: isVisible ? 0 : 20 }}
          transition={{ duration: 0.8, delay: 0.8 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12"
        >
          <Button 
            size="lg" 
            className="bg-gradient-premium hover:shadow-glow-lg text-white px-8 py-4 text-lg rounded-xl transition-all duration-300 transform hover:scale-105"
          >
            <Rocket className="w-5 h-5 mr-2" />
            Start Investigation
            <ArrowRight className="w-5 h-5 ml-2" />
          </Button>
          <Button 
            variant="outline" 
            size="lg"
            className="border-primary/30 hover:border-primary/60 px-8 py-4 text-lg rounded-xl glass transition-all duration-300"
          >
            <Play className="w-5 h-5 mr-2" />
            Watch Demo
          </Button>
        </motion.div>

        {/* Stats Preview */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: isVisible ? 1 : 0, scale: isVisible ? 1 : 0.9 }}
          transition={{ duration: 0.8, delay: 1 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto"
        >
          {[
            { value: "99.8%", label: "Detection Rate", icon: Target },
            { value: "<15s", label: "Analysis Time", icon: Clock },
            { value: "$2.8B+", label: "Threats Blocked", icon: Shield },
            { value: "150k+", label: "Users Protected", icon: Users }
          ].map((stat, index) => (
            <motion.div
              key={index}
              whileHover={{ scale: 1.05 }}
              className="glass rounded-xl p-6 text-center border border-white/10 hover:border-primary/30 transition-all duration-300"
            >
              <stat.icon className="w-8 h-8 text-primary mx-auto mb-2" />
              <div className="text-2xl font-bold text-foreground">{stat.value}</div>
              <div className="text-sm text-muted-foreground">{stat.label}</div>
            </motion.div>
          ))}
        </motion.div>
      </motion.div>

      {/* Scroll Indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5 }}
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
      >
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="text-muted-foreground cursor-pointer"
        >
          <ChevronDown className="w-6 h-6" />
        </motion.div>
      </motion.div>
    </section>
  );
};

// Advanced Features Section
const FeaturesSection = () => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, threshold: 0.1 });

  const features = [
    {
      icon: Brain,
      title: "AI-Powered Detection",
      description: "Advanced machine learning algorithms analyze patterns and behaviors to identify emerging threats in real-time.",
      color: "from-primary to-orange-600",
      stats: "99.8% accuracy"
    },
    {
      icon: Network,
      title: "Deep Investigation",
      description: "Comprehensive evidence gathering with cross-platform analysis and relationship mapping.",
      color: "from-accent to-blue-600",
      stats: "50+ data sources"
    },
    {
      icon: Fingerprint,
      title: "Behavioral Analysis",
      description: "Sophisticated pattern recognition to identify suspicious activities and predict future threats.",
      color: "from-purple-500 to-pink-600",
      stats: "Real-time monitoring"
    },
    {
      icon: Radar,
      title: "Threat Intelligence",
      description: "Global threat intelligence network providing insights into the latest scam techniques and vectors.",
      color: "from-green-500 to-emerald-600",
      stats: "Global coverage"
    },
    {
      icon: Lock,
      title: "Secure Architecture",
      description: "Enterprise-grade security with end-to-end encryption and compliance with international standards.",
      color: "from-red-500 to-rose-600",
      stats: "Bank-level security"
    },
    {
      icon: Activity,
      title: "Real-time Analytics",
      description: "Live dashboards with actionable insights and automated reporting for immediate response.",
      color: "from-cyan-500 to-teal-600",
      stats: "Sub-second alerts"
    }
  ];

  return (
    <section ref={ref} className="py-24 relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <Badge className="mb-4 bg-accent/20 text-accent border-accent/30">
            <Cpu className="w-4 h-4 mr-2" />
            Advanced AI Technology
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold mb-6 gradient-text-blue font-tech">
            Next-Generation Protection
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Harness the power of artificial intelligence to stay ahead of evolving threats 
            with our comprehensive security platform.
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ y: -10, scale: 1.02 }}
              className="group"
            >
              <Card className="h-full glass border-white/10 hover:border-primary/30 transition-all duration-500 overflow-hidden relative">
                {/* Gradient Background */}
                <div className={`absolute inset-0 bg-gradient-to-br ${feature.color} opacity-5 group-hover:opacity-10 transition-opacity duration-500`} />
                
                <CardContent className="p-8 relative z-10">
                  {/* Icon */}
                  <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} p-3 mb-6 shadow-glow`}>
                    <feature.icon className="w-8 h-8 text-white" />
                  </div>
                  
                  {/* Content */}
                  <h3 className="text-xl font-bold mb-3 text-foreground group-hover:text-primary transition-colors">
                    {feature.title}
                  </h3>
                  <p className="text-muted-foreground mb-4 leading-relaxed">
                    {feature.description}
                  </p>
                  
                  {/* Stats Badge */}
                  <Badge variant="outline" className="text-xs border-primary/30 text-primary">
                    {feature.stats}
                  </Badge>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

// AI Capabilities Showcase
const AICapabilitiesSection = () => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, threshold: 0.1 });

  const capabilities = [
    {
      category: "Detection & Analysis",
      items: [
        { name: "Deepfake Detection", confidence: 99.2 },
        { name: "Voice Cloning Analysis", confidence: 97.8 },
        { name: "Phishing URL Scanning", confidence: 99.9 },
        { name: "Social Engineering", confidence: 96.5 },
        { name: "Financial Fraud", confidence: 98.7 }
      ],
      icon: Microscope,
      color: "primary"
    },
    {
      category: "Intelligence Gathering",
      items: [
        { name: "Cross-Platform Search", confidence: 94.3 },
        { name: "Digital Footprinting", confidence: 92.1 },
        { name: "Network Analysis", confidence: 95.8 },
        { name: "Behavioral Profiling", confidence: 89.6 },
        { name: "Pattern Recognition", confidence: 96.2 }
      ],
      icon: Database,
      color: "accent"
    }
  ];

  return (
    <section ref={ref} className="py-24 bg-muted/5">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 gradient-text font-tech">
            AI Capabilities
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Real-time performance metrics from our advanced AI engine showcasing 
            industry-leading detection rates across multiple threat vectors.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {capabilities.map((category, categoryIndex) => (
            <motion.div
              key={categoryIndex}
              initial={{ opacity: 0, x: categoryIndex === 0 ? -30 : 30 }}
              animate={isInView ? { opacity: 1, x: 0 } : {}}
              transition={{ duration: 0.8, delay: categoryIndex * 0.2 }}
            >
              <Card className="glass border-white/10 p-8 h-full">
                <div className="flex items-center mb-8">
                  <div className={`w-12 h-12 rounded-lg bg-${category.color}/20 p-3 mr-4`}>
                    <category.icon className={`w-6 h-6 text-${category.color}`} />
                  </div>
                  <h3 className="text-2xl font-bold text-foreground">{category.category}</h3>
                </div>

                <div className="space-y-6">
                  {category.items.map((item, itemIndex) => (
                    <motion.div
                      key={itemIndex}
                      initial={{ opacity: 0, x: -20 }}
                      animate={isInView ? { opacity: 1, x: 0 } : {}}
                      transition={{ duration: 0.6, delay: categoryIndex * 0.2 + itemIndex * 0.1 }}
                      className="flex items-center justify-between"
                    >
                      <span className="text-foreground font-medium">{item.name}</span>
                      <div className="flex items-center space-x-3">
                        <div className="w-32 h-2 bg-muted rounded-full overflow-hidden">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={isInView ? { width: `${item.confidence}%` } : {}}
                            transition={{ duration: 1, delay: categoryIndex * 0.2 + itemIndex * 0.1 + 0.5 }}
                            className={`h-full bg-gradient-to-r from-${category.color} to-${category.color}-600 rounded-full`}
                          />
                        </div>
                        <span className={`text-sm font-bold text-${category.color} min-w-[3rem]`}>
                          {item.confidence}%
                        </span>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

// Interactive Demo Section
const InteractiveDemoSection = () => {
  const [activeDemo, setActiveDemo] = useState(0);
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, threshold: 0.1 });

  const demos = [
    {
      title: "Real-time Threat Detection",
      description: "Watch our AI identify and analyze potential threats in real-time",
      icon: Radar,
      preview: "Live scanning of 50,000+ URLs per second...",
      stats: { detected: 247, blocked: 245, processing: 1205 }
    },
    {
      title: "Evidence Collection",
      description: "Comprehensive digital forensics and evidence gathering",
      icon: FileText,
      preview: "Gathering evidence from multiple sources...",
      stats: { sources: 42, evidence: 156, confidence: 94.2 }
    },
    {
      title: "Investigation Report",
      description: "AI-generated comprehensive investigation reports",
      icon: BarChart3,
      preview: "Generating detailed analysis report...",
      stats: { pages: 23, insights: 67, recommendations: 12 }
    }
  ];

  return (
    <section ref={ref} className="py-24 relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 gradient-text-blue font-tech">
            See ScamShield in Action
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Experience the power of our AI platform with interactive demonstrations 
            of key features and capabilities.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Demo Controls */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={isInView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="space-y-4"
          >
            {demos.map((demo, index) => (
              <motion.div
                key={index}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setActiveDemo(index)}
                className={`p-6 rounded-xl cursor-pointer transition-all duration-300 border ${
                  activeDemo === index 
                    ? 'bg-primary/10 border-primary/50 shadow-glow' 
                    : 'glass border-white/10 hover:border-primary/30'
                }`}
              >
                <div className="flex items-start space-x-4">
                  <div className={`w-12 h-12 rounded-lg p-3 ${
                    activeDemo === index ? 'bg-primary text-white' : 'bg-muted text-muted-foreground'
                  } transition-colors duration-300`}>
                    <demo.icon className="w-6 h-6" />
                  </div>
                  <div className="flex-1">
                    <h3 className={`text-lg font-bold mb-2 ${
                      activeDemo === index ? 'text-primary' : 'text-foreground'
                    } transition-colors duration-300`}>
                      {demo.title}
                    </h3>
                    <p className="text-muted-foreground">{demo.description}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>

          {/* Demo Preview */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={isInView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="relative"
          >
            <Card className="glass border-white/10 p-8 min-h-[400px]">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-bold text-foreground">
                  {demos[activeDemo].title}
                </h3>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
                  <span className="text-sm text-muted-foreground">Live</span>
                </div>
              </div>

              {/* Simulated Interface */}
              <div className="space-y-4 mb-6">
                <div className="font-mono text-sm text-green-400 bg-black/20 p-3 rounded">
                  {demos[activeDemo].preview}
                </div>
                
                {/* Stats Display */}
                <div className="grid grid-cols-3 gap-4">
                  {Object.entries(demos[activeDemo].stats).map(([key, value], index) => (
                    <div key={index} className="text-center p-3 bg-muted/20 rounded-lg">
                      <div className="text-2xl font-bold text-primary">{value}</div>
                      <div className="text-xs text-muted-foreground capitalize">{key}</div>
                    </div>
                  ))}
                </div>
              </div>

              <Button className="w-full bg-gradient-premium text-white hover:shadow-glow">
                <Play className="w-4 h-4 mr-2" />
                Start Interactive Demo
              </Button>
            </Card>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

// Pricing Section
const PricingSection = () => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, threshold: 0.1 });

  const plans = [
    {
      name: "Starter",
      price: "$49",
      period: "/month",
      description: "Perfect for small businesses and individuals",
      features: [
        "Up to 100 investigations per month",
        "Basic AI threat detection",
        "Email support",
        "Standard reporting",
        "7-day data retention"
      ],
      cta: "Start Free Trial",
      popular: false,
      color: "border-white/10"
    },
    {
      name: "Professional",
      price: "$149",
      period: "/month",
      description: "Advanced protection for growing organizations",
      features: [
        "Unlimited investigations",
        "Advanced AI analysis",
        "Priority support",
        "Custom reports",
        "30-day data retention",
        "API access",
        "Team collaboration"
      ],
      cta: "Start Professional",
      popular: true,
      color: "border-primary/50 shadow-glow"
    },
    {
      name: "Enterprise",
      price: "Custom",
      period: "pricing",
      description: "Comprehensive solution for large organizations",
      features: [
        "Unlimited everything",
        "Custom AI models",
        "Dedicated support",
        "White-label reports",
        "Unlimited data retention",
        "Advanced integrations",
        "SLA guarantees",
        "On-premise deployment"
      ],
      cta: "Contact Sales",
      popular: false,
      color: "border-accent/30"
    }
  ];

  return (
    <section ref={ref} className="py-24 bg-muted/5">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 gradient-text font-tech">
            Choose Your Protection Level
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Flexible pricing plans designed to scale with your security needs. 
            All plans include our core AI protection features.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {plans.map((plan, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ y: -10, scale: 1.02 }}
              className="relative"
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <Badge className="bg-gradient-premium text-white px-4 py-1 shadow-glow">
                    <Star className="w-3 h-3 mr-1" />
                    Most Popular
                  </Badge>
                </div>
              )}

              <Card className={`h-full glass p-8 ${plan.color} transition-all duration-500 hover:shadow-premium`}>
                <CardContent className="p-0">
                  <div className="text-center mb-8">
                    <h3 className="text-2xl font-bold text-foreground mb-2">{plan.name}</h3>
                    <div className="flex items-baseline justify-center mb-2">
                      <span className="text-4xl font-bold text-primary">{plan.price}</span>
                      <span className="text-muted-foreground ml-1">{plan.period}</span>
                    </div>
                    <p className="text-muted-foreground">{plan.description}</p>
                  </div>

                  <ul className="space-y-3 mb-8">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-start">
                        <CheckCircle className="w-5 h-5 text-primary mr-3 mt-0.5 flex-shrink-0" />
                        <span className="text-foreground">{feature}</span>
                      </li>
                    ))}
                  </ul>

                  <Button 
                    className={`w-full ${
                      plan.popular 
                        ? 'bg-gradient-premium text-white hover:shadow-glow-lg' 
                        : 'bg-transparent border border-primary/30 hover:bg-primary/10'
                    } transition-all duration-300`}
                    size="lg"
                  >
                    {plan.cta}
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

// Main Component
const ModernLandingPage = () => {
  return (
    <div className="min-h-screen bg-background text-foreground overflow-x-hidden">
      <HeroSection />
      <FeaturesSection />
      <AICapabilitiesSection />
      <InteractiveDemoSection />
      <PricingSection />
    </div>
  );
};

export default ModernLandingPage;
