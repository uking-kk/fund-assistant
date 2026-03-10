import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useChat } from '../hooks/useChat'
import MessageList from './MessageList'
import { Send, Loader2, Sparkles, Bot } from 'lucide-react'

const QUICK_QUESTIONS = [
  "什么是ETF基金？",
  "如何选择适合自己的基金？",
  "定投和一次性买入哪个好？",
  "推荐几只稳健的基金"
]

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
}

export default function ChatWindow() {
  const [input, setInput] = useState('')
  const { messages, sendMessage, isLoading } = useChat()
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return
    
    await sendMessage(input)
    setInput('')
    inputRef.current?.focus()
  }

  const handleQuickQuestion = async (question) => {
    setInput('')
    await sendMessage(question)
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 scrollbar-thin">
        <MessageList messages={messages} />
        <div ref={messagesEndRef} />
        
        {messages.length === 1 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.3 }}
            className="mt-6"
          >
            <p className="text-sm text-gray-500 mb-4 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-primary-500" />
              你可以问我这些问题
            </p>
            <motion.div 
              className="flex flex-wrap gap-2"
              variants={containerVariants}
              initial="hidden"
              animate="visible"
            >
              {QUICK_QUESTIONS.map((q, i) => (
                <motion.button
                  key={i}
                  variants={itemVariants}
                  whileHover={{ scale: 1.02, y: -2 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => handleQuickQuestion(q)}
                  disabled={isLoading}
                  className="px-4 py-2 text-sm bg-white border border-gray-200 rounded-xl hover:border-primary-400 hover:bg-primary-50 hover:shadow-md transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                >
                  {q}
                </motion.button>
              ))}
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="mt-6 p-4 bg-gradient-to-r from-primary-50 to-blue-50 rounded-2xl border border-primary-100"
            >
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <Bot className="w-5 h-5 text-primary-600" />
                </div>
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-1">我能帮你做什么？</h4>
                  <ul className="text-xs text-gray-600 space-y-1">
                    <li>• 解答基金投资相关问题</li>
                    <li>• 查询基金净值、收益等数据</li>
                    <li>• 推荐适合你的基金产品</li>
                  </ul>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="p-4 bg-white border-t border-gray-100">
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="输入你的问题..."
              disabled={isLoading}
              className="w-full px-4 py-3.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent focus:bg-white disabled:bg-gray-100 disabled:cursor-not-allowed transition-all duration-200 placeholder:text-gray-400"
            />
            {isLoading && (
              <div className="absolute right-4 top-1/2 -translate-y-1/2">
                <motion.div
                  animate={{ opacity: [0.5, 1, 0.5] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                  className="text-xs text-gray-400"
                >
                  思考中...
                </motion.div>
              </div>
            )}
          </div>
          <motion.button
            type="submit"
            disabled={isLoading || !input.trim()}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="px-6 py-3.5 bg-primary-600 text-white rounded-xl hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center gap-2 font-medium shadow-sm hover:shadow-md cursor-pointer"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
            <span className="hidden sm:inline">发送</span>
          </motion.button>
        </div>
      </form>
    </div>
  )
}
