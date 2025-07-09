import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Separator } from '../ui/separator';
import { Checkbox } from '../ui/checkbox';
import { Alert, AlertDescription } from '../ui/alert';
import { 
  Mail, Lock, Eye, EyeOff, ArrowRight, AlertCircle, 
  Chrome, Github, Apple, Loader2 
} from 'lucide-react';
import PremiumAuthLayout from './PremiumAuthLayout';

const PremiumLoginForm = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { signIn } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const { data, error } = await signIn(formData.email, formData.password);
      if (error) {
        setError(error.message || 'Failed to sign in. Please check your credentials.');
      } else if (data) {
        navigate('/dashboard');
      }
    } catch (error) {
      setError(error.message || 'Failed to sign in. Please check your credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSocialLogin = (provider) => {
    // Implement social login logic here
    console.log(`Login with ${provider}`);
  };

  const socialProviders = [
    { name: 'Google', icon: Chrome, color: 'hover:bg-red-500/10 hover:border-red-500/30' },
    { name: 'GitHub', icon: Github, color: 'hover:bg-gray-500/10 hover:border-gray-500/30' },
    { name: 'Apple', icon: Apple, color: 'hover:bg-gray-500/10 hover:border-gray-500/30' }
  ];

  return (
    <PremiumAuthLayout
      title="Sign In"
      subtitle="Access your security command center"
      type="login"
    >
      <form onSubmit={handleSubmit} className="space-y-6">
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <Alert variant="destructive" className="glass border-red-500/50">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          </motion.div>
        )}

        {/* Social Login */}
        <div className="space-y-4">
          <div className="grid grid-cols-3 gap-3">
            {socialProviders.map((provider, index) => (
              <motion.button
                key={provider.name}
                type="button"
                onClick={() => handleSocialLogin(provider.name.toLowerCase())}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`
                  flex items-center justify-center p-3 border border-white/20 rounded-xl 
                  glass transition-all duration-300 ${provider.color}
                `}
              >
                <provider.icon className="w-5 h-5" />
              </motion.button>
            ))}
          </div>
          
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <Separator className="w-full opacity-30" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-background px-2 text-muted-foreground">
                Or continue with email
              </span>
            </div>
          </div>
        </div>

        {/* Email Field */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="space-y-2"
        >
          <Label htmlFor="email" className="text-sm font-medium text-foreground">
            Email Address
          </Label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <Input
              id="email"
              name="email"
              type="email"
              required
              value={formData.email}
              onChange={handleChange}
              className="pl-10 glass border-white/20 focus:border-primary/50 focus:ring-primary/20"
              placeholder="Enter your email"
            />
          </div>
        </motion.div>

        {/* Password Field */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="space-y-2"
        >
          <Label htmlFor="password" className="text-sm font-medium text-foreground">
            Password
          </Label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <Input
              id="password"
              name="password"
              type={showPassword ? 'text' : 'password'}
              required
              value={formData.password}
              onChange={handleChange}
              className="pl-10 pr-10 glass border-white/20 focus:border-primary/50 focus:ring-primary/20"
              placeholder="Enter your password"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
            >
              {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          </div>
        </motion.div>

        {/* Remember Me & Forgot Password */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="flex items-center justify-between"
        >
          <div className="flex items-center space-x-2">
            <Checkbox
              id="rememberMe"
              name="rememberMe"
              checked={formData.rememberMe}
              onCheckedChange={(checked) => 
                setFormData(prev => ({ ...prev, rememberMe: checked }))
              }
              className="border-white/30"
            />
            <Label 
              htmlFor="rememberMe" 
              className="text-sm text-muted-foreground cursor-pointer"
            >
              Remember me
            </Label>
          </div>
          <Link 
            to="/forgot-password" 
            className="text-sm text-primary hover:text-primary/80 transition-colors"
          >
            Forgot password?
          </Link>
        </motion.div>

        {/* Submit Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-premium hover:shadow-glow-lg text-white py-3 text-base font-medium rounded-xl transition-all duration-300"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Signing In...
              </>
            ) : (
              <>
                Sign In
                <ArrowRight className="w-5 h-5 ml-2" />
              </>
            )}
          </Button>
        </motion.div>

        {/* Sign Up Link */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="text-center"
        >
          <p className="text-sm text-muted-foreground">
            Don't have an account?{' '}
            <Link 
              to="/signup" 
              className="text-primary hover:text-primary/80 font-medium transition-colors"
            >
              Create one now
            </Link>
          </p>
        </motion.div>
      </form>

      {/* Demo Credentials */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="mt-6 p-4 glass rounded-xl border border-accent/30"
      >
        <div className="text-center">
          <p className="text-xs text-muted-foreground mb-2">Demo Credentials</p>
          <div className="text-xs space-y-1">
            <div className="text-accent">Email: demo@scamshield.ai</div>
            <div className="text-accent">Password: demo123</div>
          </div>
        </div>
      </motion.div>
    </PremiumAuthLayout>
  );
};

export default PremiumLoginForm;
