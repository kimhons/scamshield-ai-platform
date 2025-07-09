import React from 'react';
import { motion } from 'framer-motion';
import { Shield, Sparkles, Lock, Brain, Zap } from 'lucide-react';
import { Card, CardContent } from '../ui/card';

const PremiumAuthLayout = ({ children, title, subtitle, type = 'login' }) => {
  const features = [
    {
      icon: Brain,
      title: "AI-Powered Detection",
      description: "Advanced machine learning algorithms"
    },
    {
      icon: Lock,
      title: "Enterprise Security",
      description: "Bank-level encryption and protection"
    },
    {
      icon: Zap,
      title: "Real-time Analysis",
      description: "Instant threat detection and response"
    }
  ];

  return (
    <div className="min-h-screen bg-background relative overflow-hidden flex items-center justify-center">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-background via-muted/10 to-background">
        <div className="absolute inset-0 bg-noise opacity-20"></div>
        <motion.div 
          className="absolute top-20 left-20 w-96 h-96 bg-primary/10 rounded-full blur-3xl"
          animate={{ scale: [1, 1.2, 1], rotate: [0, 180, 360] }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        />
        <motion.div 
          className="absolute bottom-20 right-20 w-80 h-80 bg-accent/10 rounded-full blur-3xl"
          animate={{ scale: [1.2, 1, 1.2], rotate: [360, 180, 0] }}
          transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
        />
      </div>

      <div className="relative z-10 w-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Side - Branding & Features */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center lg:text-left"
          >
            {/* Logo */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="flex items-center justify-center lg:justify-start mb-8"
            >
              <div className="w-16 h-16 bg-gradient-premium rounded-2xl p-4 shadow-glow mr-4">
                <Shield className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold gradient-text font-tech">ScamShield</h1>
                <p className="text-sm text-muted-foreground">AI Security Platform</p>
              </div>
            </motion.div>

            {/* Main Heading */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="mb-8"
            >
              <h2 className="text-4xl lg:text-5xl font-bold text-foreground mb-4 leading-tight">
                {type === 'login' ? 'Welcome Back' : 'Join ScamShield'}
              </h2>
              <p className="text-xl text-muted-foreground leading-relaxed">
                {type === 'login' 
                  ? 'Access your AI-powered security command center and protect your digital assets with advanced threat detection.'
                  : 'Create your account to start protecting against sophisticated scams and fraud with our AI platform.'
                }
              </p>
            </motion.div>

            {/* Features */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="space-y-6 hidden lg:block"
            >
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.8 + index * 0.1 }}
                  className="flex items-start space-x-4"
                >
                  <div className="w-12 h-12 bg-muted/20 rounded-xl p-3 flex-shrink-0">
                    <feature.icon className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-foreground mb-1">
                      {feature.title}
                    </h3>
                    <p className="text-muted-foreground">
                      {feature.description}
                    </p>
                  </div>
                </motion.div>
              ))}
            </motion.div>

            {/* Trust Indicators */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.2 }}
              className="mt-12 hidden lg:block"
            >
              <div className="flex items-center space-x-8 text-sm text-muted-foreground">
                <div className="flex items-center space-x-2">
                  <Shield className="w-4 h-4 text-green-500" />
                  <span>SOC 2 Compliant</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Lock className="w-4 h-4 text-green-500" />
                  <span>256-bit Encryption</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Sparkles className="w-4 h-4 text-green-500" />
                  <span>99.9% Uptime</span>
                </div>
              </div>
            </motion.div>
          </motion.div>

          {/* Right Side - Auth Form */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="w-full max-w-md mx-auto lg:mx-0"
          >
            <Card className="glass border-white/10 shadow-premium backdrop-blur-xl">
              <CardContent className="p-8">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  className="text-center mb-8"
                >
                  <h3 className="text-2xl font-bold text-foreground mb-2">
                    {title}
                  </h3>
                  <p className="text-muted-foreground">
                    {subtitle}
                  </p>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6 }}
                >
                  {children}
                </motion.div>
              </CardContent>
            </Card>

            {/* Mobile Features */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
              className="mt-8 lg:hidden"
            >
              <div className="grid grid-cols-1 gap-4">
                {features.map((feature, index) => (
                  <div key={index} className="flex items-center space-x-3 p-4 glass rounded-xl border border-white/10">
                    <div className="w-10 h-10 bg-muted/20 rounded-lg p-2">
                      <feature.icon className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h3 className="text-sm font-semibold text-foreground">
                        {feature.title}
                      </h3>
                      <p className="text-xs text-muted-foreground">
                        {feature.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default PremiumAuthLayout;
