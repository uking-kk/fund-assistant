import { motion } from 'framer-motion'
import ChatWindow from './components/ChatWindow'
import { Bot, Sparkles, TrendingUp, Shield, Zap } from 'lucide-react'

const features = [
  { icon: TrendingUp, text: '基金数据查询', color: 'text-green-500' },
  { icon: Shield, text: '投资知识问答', color: 'text-blue-500' },
  { icon: Zap, text: '智能推荐', color: 'text-purple-500' },
]

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/50">
      <div className="container mx-auto max-w-4xl h-screen flex flex-col">
        <motion.header
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.4, ease: "easeOut" }}
          className="flex items-center gap-4 p-4 border-b border-gray-100/80 bg-white/60 backdrop-blur-xl sticky top-0 z-10"
        >
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ 
              type: "spring", 
              stiffness: 500, 
              damping: 25,
              delay: 0.1 
            }}
            className="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center shadow-lg shadow-primary-500/25"
          >
            <Bot className="w-7 h-7 text-white" />
          </motion.div>
          <div className="flex-1">
            <motion.h1 
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="text-xl font-bold text-gray-900 tracking-tight"
            >
              基金智能助手
            </motion.h1>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="flex items-center gap-1.5"
            >
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
              </span>
              <p className="text-xs text-gray-500">基于大模型的基金投资问答助手</p>
            </motion.div>
          </div>
          
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="hidden sm:flex items-center gap-3"
          >
            {features.map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + i * 0.1 }}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-white rounded-full border border-gray-100 shadow-sm"
              >
                <feature.icon className={`w-3.5 h-3.5 ${feature.color}`} />
                <span className="text-xs text-gray-600">{feature.text}</span>
              </motion.div>
            ))}
          </motion.div>
        </motion.header>
        
        <main className="flex-1 overflow-hidden">
          <ChatWindow />
        </main>
        
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="py-2 px-4 text-center border-t border-gray-100/50 bg-white/40 backdrop-blur-sm"
        >
          <p className="text-xs text-gray-400">
            Powered by 火山方舟 · 豆包大模型
          </p>
        </motion.footer>
      </div>
    </div>
  )
}

export default App
