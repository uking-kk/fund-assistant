import { motion, AnimatePresence } from 'framer-motion'
import { User, Bot, Copy, Check, Volume2 } from 'lucide-react'
import { useState } from 'react'

const messageVariants = {
  hidden: { opacity: 0, y: 10, scale: 0.95 },
  visible: { 
    opacity: 1, 
    y: 0, 
    scale: 1,
    transition: { type: "spring", stiffness: 500, damping: 30 }
  },
  exit: { 
    opacity: 0, 
    y: -10,
    transition: { duration: 0.2 }
  }
}

const typingVariants = {
  initial: { opacity: 0.3 },
  animate: { 
    opacity: [0.3, 1, 0.3],
    transition: { duration: 1.5, repeat: Infinity }
  }
}

export default function MessageList({ messages }) {
  return (
    <div className="space-y-5">
      <AnimatePresence mode="popLayout">
        {messages.map((msg, index) => (
          <motion.div
            key={index}
            variants={messageVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
            layout
            className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.1, type: "spring", stiffness: 500 }}
              className={`w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 shadow-sm ${
                msg.role === 'user'
                  ? 'bg-gradient-to-br from-primary-500 to-primary-600 text-white'
                  : 'bg-gradient-to-br from-gray-100 to-gray-200 text-gray-600'
              }`}
            >
              {msg.role === 'user' ? (
                <User className="w-5 h-5" />
              ) : (
                <Bot className="w-5 h-5" />
              )}
            </motion.div>
            
            <div className={`max-w-[85%] ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <motion.div
                initial={{ scale: 0.9 }}
                animate={{ scale: 1 }}
                className={`relative px-4 py-3 rounded-2xl shadow-sm ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-br from-primary-500 to-primary-600 text-white rounded-tr-sm'
                    : 'bg-white border border-gray-100 text-gray-700 rounded-tl-sm'
                }`}
              >
                <p className="text-sm leading-relaxed whitespace-pre-wrap">
                  {msg.content}
                  {msg.role === 'assistant' && !msg.content && (
                    <span className="flex gap-1">
                      <motion.span variants={typingVariants} initial="initial" animate="animate">●</motion.span>
                      <motion.span variants={typingVariants} initial="initial" animate="animate" transition={{ delay: 0.2 }}>●</motion.span>
                      <motion.span variants={typingVariants} initial="initial" animate="animate" transition={{ delay: 0.4 }}>●</motion.span>
                    </span>
                  )}
                </p>
                
                {msg.role === 'assistant' && msg.content && (
                  <div className="absolute -bottom-8 left-0 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button className="p-1.5 hover:bg-gray-100 rounded-lg transition-colors">
                      <Copy className="w-3.5 h-3.5 text-gray-400" />
                    </button>
                  </div>
                )}
              </motion.div>
              
              {msg.role === 'assistant' && msg.content && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                  className="flex items-center gap-2 mt-2 ml-1"
                >
                  <span className="text-xs text-gray-400">AI助手</span>
                </motion.div>
              )}
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  )
}

function TypingIndicator() {
  return (
    <div className="flex gap-1.5 px-2 py-3">
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          animate={{
            y: [0, -5, 0],
            opacity: [0.4, 1, 0.4]
          }}
          transition={{
            duration: 0.6,
            repeat: Infinity,
            delay: i * 0.15
          }}
          className="w-2 h-2 bg-gray-400 rounded-full"
        />
      ))}
    </div>
  )
}
