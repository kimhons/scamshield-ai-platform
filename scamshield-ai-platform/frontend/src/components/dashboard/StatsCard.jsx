import React from 'react'
import { Card, CardContent } from '../ui/card'
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown } from 'lucide-react'

const StatsCard = ({ title, value, change, icon: Icon, gradient, index = 0 }) => {
  const isPositive = change && change.startsWith('+')
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
    >
      <Card className="bg-black/40 backdrop-blur-xl border-white/10 hover:border-orange-500/30 transition-all duration-300 transform hover:scale-105">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm font-medium">{title}</p>
              <p className="text-2xl font-bold text-white mt-1">{value}</p>
              {change && (
                <div className={`flex items-center mt-2 text-sm ${
                  isPositive ? 'text-green-400' : 'text-red-400'
                }`}>
                  {isPositive ? (
                    <TrendingUp className="w-4 h-4 mr-1" />
                  ) : (
                    <TrendingDown className="w-4 h-4 mr-1" />
                  )}
                  <span>{change}</span>
                </div>
              )}
            </div>
            <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${gradient} flex items-center justify-center`}>
              <Icon className="w-6 h-6 text-white" />
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

export default StatsCard