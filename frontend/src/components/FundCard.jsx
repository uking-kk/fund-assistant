import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, Minus, BarChart3, Users, Calendar, Shield } from 'lucide-react'

export default function FundCard({ data }) {
  if (!data) return null

  const getTrendIcon = (value) => {
    if (!value) return <Minus className="w-4 h-4" />
    const num = parseFloat(value)
    if (num > 0) return <TrendingUp className="w-4 h-4 text-green-500" />
    if (num < 0) return <TrendingDown className="w-4 h-4 text-red-500" />
    return <Minus className="w-4 h-4 text-gray-400" />
  }

  const getTrendColor = (value) => {
    if (!value) return 'text-gray-400'
    const num = parseFloat(value)
    if (num > 0) return 'text-green-600'
    if (num < 0) return 'text-red-600'
    return 'text-gray-400'
  }

  const formatPercent = (value) => {
    if (!value) return '--'
    const num = parseFloat(value)
    return `${num >= 0 ? '+' : ''}${num.toFixed(2)}%`
  }

  const formatScale = (value) => {
    if (!value) return '--'
    const num = parseFloat(value)
    if (num >= 100) return `${(num / 100).toFixed(2)}亿`
    return `${num.toFixed(2)}亿`
  }

  const getRiskColor = (level) => {
    const colors = {
      '低风险': 'bg-green-100 text-green-700',
      '中低风险': 'bg-lime-100 text-lime-700',
      '中风险': 'bg-yellow-100 text-yellow-700',
      '中高风险': 'bg-orange-100 text-orange-700',
      '高风险': 'bg-red-100 text-red-700',
    }
    return colors[level] || 'bg-gray-100 text-gray-700'
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden"
    >
      <div className="p-5 border-b border-gray-50">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{data.name}</h3>
            <p className="text-sm text-gray-500 mt-1">{data.code}</p>
          </div>
          <div className="flex items-center gap-2">
            {data.type && (
              <span className="px-2.5 py-1 text-xs font-medium bg-blue-50 text-blue-700 rounded-full">
                {data.type}
              </span>
            )}
            {data.risk_level && (
              <span className={`px-2.5 py-1 text-xs font-medium rounded-full ${getRiskColor(data.risk_level)}`}>
                {data.risk_level}
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="p-5">
        <div className="grid grid-cols-2 gap-4 mb-5">
          <div className="space-y-1">
            <p className="text-xs text-gray-500">近1年收益</p>
            <div className="flex items-center gap-2">
              {getTrendIcon(data.returns?.['1y'])}
              <span className={`text-xl font-bold ${getTrendColor(data.returns?.['1y'])}`}>
                {formatPercent(data.returns?.['1y'])}
              </span>
            </div>
          </div>
          <div className="space-y-1">
            <p className="text-xs text-gray-500">近3年收益</p>
            <div className="flex items-center gap-2">
              {getTrendIcon(data.returns?.['3y'])}
              <span className={`text-xl font-bold ${getTrendColor(data.returns?.['3y'])}`}>
                {formatPercent(data.returns?.['3y'])}
              </span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-3 mb-5">
          <div className="bg-gray-50 rounded-xl p-3 text-center">
            <BarChart3 className="w-4 h-4 text-gray-400 mx-auto mb-1" />
            <p className="text-xs text-gray-500">基金规模</p>
            <p className="text-sm font-semibold text-gray-900 mt-1">
              {formatScale(data.scale)}
            </p>
          </div>
          <div className="bg-gray-50 rounded-xl p-3 text-center">
            <Users className="w-4 h-4 text-gray-400 mx-auto mb-1" />
            <p className="text-xs text-gray-500">基金经理</p>
            <p className="text-sm font-semibold text-gray-900 mt-1 truncate">
              {data.manager || '--'}
            </p>
          </div>
          <div className="bg-gray-50 rounded-xl p-3 text-center">
            <Calendar className="w-4 h-4 text-gray-400 mx-auto mb-1" />
            <p className="text-xs text-gray-500">最新净值</p>
            <p className="text-sm font-semibold text-gray-900 mt-1">
              {data.net_value || '--'}
            </p>
          </div>
        </div>

        <div className="bg-gradient-to-r from-gray-50 to-gray-50/50 rounded-xl p-4">
          <div className="flex items-center justify-between text-xs text-gray-500 mb-2">
            <span>收益走势</span>
            <span>近6个月</span>
          </div>
          <div className="flex items-end gap-1 h-12">
            {[data.returns?.['1m'], data.returns?.['3m'], data.returns?.['6m']].map((val, i) => {
              const height = val ? Math.min(Math.max(Math.abs(parseFloat(val)) * 3, 10), 100) : 20
              const isPositive = val && parseFloat(val) >= 0
              return (
                <motion.div
                  key={i}
                  initial={{ height: 0 }}
                  animate={{ height: `${height}%` }}
                  transition={{ delay: i * 0.1, duration: 0.3 }}
                  className={`flex-1 rounded-t ${
                    isPositive ? 'bg-green-400' : 'bg-red-400'
                  }`}
                />
              )
            })}
          </div>
          <div className="flex justify-between text-xs text-gray-400 mt-2">
            <span>1月</span>
            <span>3月</span>
            <span>6月</span>
          </div>
        </div>
      </div>

      {data.company && (
        <div className="px-5 py-3 bg-gray-50 border-t border-gray-100">
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <Shield className="w-3.5 h-3.5" />
            <span>基金公司：{data.company}</span>
          </div>
        </div>
      )}
    </motion.div>
  )
}
