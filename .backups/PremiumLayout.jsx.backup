import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import {
  Shield, Home, Search, BarChart3, FileText, Settings, User, LogOut,
  Menu, X, Bell, ChevronDown, Sparkles, Zap, Brain, Globe,
  Moon, Sun, Monitor
} from 'lucide-react';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '../ui/dropdown-menu';
import { Separator } from '../ui/separator';

// Enhanced Navigation Item Component
const NavItem = ({ icon: Icon, label, path, isActive, notifications, isCollapsed }) => {
  const navigate = useNavigate();
  
  return (
    <motion.button
      onClick={() => navigate(path)}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={`
        w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-left transition-all duration-300
        ${isActive 
          ? 'bg-gradient-to-r from-primary/20 to-primary/10 text-primary border border-primary/30 shadow-glow' 
          : 'hover:bg-white/5 text-muted-foreground hover:text-foreground'
        }
        ${isCollapsed ? 'justify-center px-2' : ''}
      `}
    >
      <div className="relative">
        <Icon className={`${isCollapsed ? 'w-6 h-6' : 'w-5 h-5'} flex-shrink-0`} />
        {notifications > 0 && (
          <div className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full animate-pulse" />
        )}
      </div>
      {!isCollapsed && (
        <>
          <span className="font-medium">{label}</span>
          {notifications > 0 && (
            <Badge variant="destructive" className="ml-auto text-xs px-1.5 py-0.5 h-5">
              {notifications > 99 ? '99+' : notifications}
            </Badge>
          )}
        </>
      )}
    </motion.button>
  );
};

// Theme Toggle Component
const ThemeToggle = () => {
  const [theme, setTheme] = useState('dark');

  const toggleTheme = (newTheme) => {
    setTheme(newTheme);
    // Implement theme switching logic here
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="sm" className="w-10 h-10 rounded-full">
          {theme === 'dark' ? (
            <Moon className="w-4 h-4" />
          ) : theme === 'light' ? (
            <Sun className="w-4 h-4" />
          ) : (
            <Monitor className="w-4 h-4" />
          )}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-32 glass border-white/10">
        <DropdownMenuItem onClick={() => toggleTheme('light')}>
          <Sun className="w-4 h-4 mr-2" />
          Light
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => toggleTheme('dark')}>
          <Moon className="w-4 h-4 mr-2" />
          Dark
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => toggleTheme('system')}>
          <Monitor className="w-4 h-4 mr-2" />
          System
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};

// Premium Sidebar Component
const PremiumSidebar = ({ isCollapsed, onToggleCollapse }) => {
  const location = useLocation();
  const { user, logout } = useAuth();

  const navigationItems = [
    { icon: Home, label: 'Dashboard', path: '/dashboard', notifications: 0 },
    { icon: Search, label: 'Investigations', path: '/investigations', notifications: 3 },
    { icon: BarChart3, label: 'Analytics', path: '/analytics', notifications: 0 },
    { icon: FileText, label: 'Reports', path: '/reports', notifications: 1 },
    { icon: Settings, label: 'Settings', path: '/settings', notifications: 0 },
  ];

  return (
    <motion.div
      initial={{ x: -300 }}
      animate={{ x: 0, width: isCollapsed ? 80 : 280 }}
      transition={{ duration: 0.3, ease: "easeInOut" }}
      className="fixed left-0 top-0 h-full glass border-r border-white/10 z-40 backdrop-blur-xl"
    >
      <div className="flex flex-col h-full">
        {/* Logo Section */}
        <div className={`p-6 ${isCollapsed ? 'px-4' : ''}`}>
          <motion.div
            className="flex items-center space-x-3"
            animate={{ justifyContent: isCollapsed ? 'center' : 'flex-start' }}
          >
            <div className="w-10 h-10 bg-gradient-premium rounded-xl p-2 shadow-glow">
              <Shield className="w-6 h-6 text-white" />
            </div>
            {!isCollapsed && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                <h1 className="text-xl font-bold gradient-text font-tech">ScamShield</h1>
                <p className="text-xs text-muted-foreground">AI Security Platform</p>
              </motion.div>
            )}
          </motion.div>
        </div>

        {/* Navigation */}
        <nav className={`flex-1 ${isCollapsed ? 'px-2' : 'px-4'} space-y-2`}>
          {navigationItems.map((item, index) => (
            <NavItem
              key={item.path}
              {...item}
              isActive={location.pathname === item.path}
              isCollapsed={isCollapsed}
            />
          ))}
        </nav>

        {/* User Section */}
        <div className={`p-4 border-t border-white/10 ${isCollapsed ? 'px-2' : ''}`}>
          {isCollapsed ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="w-full h-12 p-0">
                  <Avatar className="w-8 h-8">
                    <AvatarImage src={user?.avatar} />
                    <AvatarFallback className="bg-primary text-primary-foreground">
                      {user?.email?.charAt(0).toUpperCase()}
                    </AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent side="right" className="w-48 glass border-white/10">
                <DropdownMenuLabel>
                  <div className="text-sm">
                    <div className="font-medium">{user?.email}</div>
                    <div className="text-muted-foreground text-xs">Premium User</div>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem>
                  <User className="w-4 h-4 mr-2" />
                  Profile
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <Settings className="w-4 h-4 mr-2" />
                  Settings
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={logout}>
                  <LogOut className="w-4 h-4 mr-2" />
                  Sign Out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <div className="flex items-center space-x-3 p-3 rounded-xl glass hover:bg-white/5 transition-colors">
              <Avatar className="w-10 h-10">
                <AvatarImage src={user?.avatar} />
                <AvatarFallback className="bg-primary text-primary-foreground">
                  {user?.email?.charAt(0).toUpperCase()}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-foreground truncate">
                  {user?.email}
                </div>
                <div className="text-xs text-muted-foreground">Premium User</div>
              </div>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                    <ChevronDown className="w-4 h-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-48 glass border-white/10">
                  <DropdownMenuItem>
                    <User className="w-4 h-4 mr-2" />
                    Profile
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Settings className="w-4 h-4 mr-2" />
                    Settings
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={logout}>
                    <LogOut className="w-4 h-4 mr-2" />
                    Sign Out
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          )}
        </div>

        {/* Toggle Button */}
        <div className={`p-2 ${isCollapsed ? 'flex justify-center' : 'flex justify-end'}`}>
          <Button
            variant="ghost"
            size="sm"
            onClick={onToggleCollapse}
            className="w-8 h-8 p-0 hover:bg-white/10"
          >
            <motion.div
              animate={{ rotate: isCollapsed ? 180 : 0 }}
              transition={{ duration: 0.3 }}
            >
              <ChevronDown className="w-4 h-4 rotate-90" />
            </motion.div>
          </Button>
        </div>
      </div>
    </motion.div>
  );
};

// Premium Header Component
const PremiumHeader = ({ onToggleSidebar, isSidebarCollapsed }) => {
  const [notifications] = useState([
    { id: 1, title: 'High-priority threat detected', time: '2 min ago', type: 'alert' },
    { id: 2, title: 'Investigation completed', time: '5 min ago', type: 'success' },
    { id: 3, title: 'System update available', time: '1 hour ago', type: 'info' },
  ]);

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
      className="glass border-b border-white/10 backdrop-blur-xl sticky top-0 z-30"
    >
      <div className="flex items-center justify-between px-6 py-4">
        {/* Left Section */}
        <div className="flex items-center space-x-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={onToggleSidebar}
            className="lg:hidden w-10 h-10 p-0"
          >
            <Menu className="w-5 h-5" />
          </Button>
          
          {/* Breadcrumb or Page Title */}
          <div className="hidden md:block">
            <div className="flex items-center space-x-2 text-sm text-muted-foreground">
              <span>Security Center</span>
              <span>/</span>
              <span className="text-foreground font-medium">Dashboard</span>
            </div>
          </div>
        </div>

        {/* Center Section - Search */}
        <div className="hidden md:flex flex-1 max-w-md mx-8">
          <div className="relative w-full">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search investigations, threats, reports..."
              className="w-full pl-10 pr-4 py-2 bg-muted/20 border border-white/10 rounded-xl text-sm placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-colors"
            />
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center space-x-2">
          {/* AI Status Indicator */}
          <div className="hidden lg:flex items-center space-x-2 px-3 py-1.5 rounded-full bg-green-500/20 border border-green-500/30">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-xs text-green-400 font-medium">AI Online</span>
          </div>

          {/* Notifications */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm" className="relative w-10 h-10 p-0">
                <Bell className="w-5 h-5" />
                {notifications.length > 0 && (
                  <div className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center">
                    <span className="text-xs text-white font-medium">
                      {notifications.length > 9 ? '9+' : notifications.length}
                    </span>
                  </div>
                )}
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-80 glass border-white/10 p-0">
              <DropdownMenuLabel className="px-4 py-3 border-b border-white/10">
                <div className="flex items-center justify-between">
                  <span>Notifications</span>
                  <Badge variant="secondary" className="text-xs">
                    {notifications.length} new
                  </Badge>
                </div>
              </DropdownMenuLabel>
              <div className="max-h-80 overflow-y-auto">
                {notifications.map((notification, index) => (
                  <div
                    key={notification.id}
                    className="p-4 hover:bg-white/5 transition-colors border-b border-white/5 last:border-0"
                  >
                    <div className="flex items-start space-x-3">
                      <div className={`w-2 h-2 rounded-full mt-2 ${
                        notification.type === 'alert' ? 'bg-red-500' :
                        notification.type === 'success' ? 'bg-green-500' : 'bg-blue-500'
                      }`} />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-foreground">
                          {notification.title}
                        </p>
                        <p className="text-xs text-muted-foreground mt-1">
                          {notification.time}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="p-3 border-t border-white/10">
                <Button variant="ghost" className="w-full text-sm">
                  View all notifications
                </Button>
              </div>
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Theme Toggle */}
          <ThemeToggle />
        </div>
      </div>
    </motion.header>
  );
};

// Main Premium Layout Component
const PremiumLayout = ({ children }) => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  const toggleSidebar = () => setIsSidebarCollapsed(!isSidebarCollapsed);
  const toggleMobileSidebar = () => setIsMobileSidebarOpen(!isMobileSidebarOpen);

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Background Effects */}
      <div className="fixed inset-0 bg-gradient-to-br from-background via-muted/5 to-background pointer-events-none" />
      <div className="fixed inset-0 bg-noise opacity-20 pointer-events-none" />

      {/* Mobile Sidebar Overlay */}
      <AnimatePresence>
        {isMobileSidebarOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={toggleMobileSidebar}
            className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          />
        )}
      </AnimatePresence>

      {/* Sidebar - Desktop */}
      <div className="hidden lg:block">
        <PremiumSidebar 
          isCollapsed={isSidebarCollapsed} 
          onToggleCollapse={toggleSidebar}
        />
      </div>

      {/* Sidebar - Mobile */}
      <AnimatePresence>
        {isMobileSidebarOpen && (
          <div className="lg:hidden">
            <PremiumSidebar 
              isCollapsed={false} 
              onToggleCollapse={() => {}}
            />
          </div>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <div 
        className={`min-h-screen transition-all duration-300 lg:ml-${isSidebarCollapsed ? '20' : '70'}`}
        style={{ 
          marginLeft: window.innerWidth >= 1024 ? (isSidebarCollapsed ? '80px' : '280px') : '0' 
        }}
      >
        <PremiumHeader 
          onToggleSidebar={toggleMobileSidebar}
          isSidebarCollapsed={isSidebarCollapsed}
        />
        
        <main className="relative z-10">
          {children}
        </main>
      </div>
    </div>
  );
};

export default PremiumLayout;
