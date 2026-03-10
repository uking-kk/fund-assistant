import { useState, useCallback } from 'react'
import { streamChat } from '../lib/api'

const API_URL = import.meta.env.VITE_API_URL || ''

export function useChat() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '你好！我是基金智能助手，可以帮你解答基金投资相关的问题。请问有什么可以帮你的？'
    }
  ])
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = useCallback(async (content) => {
    setMessages(prev => [...prev, { role: 'user', content }])
    setIsLoading(true)

    setMessages(prev => [...prev, { role: 'assistant', content: '' }])

    try {
      await streamChat(content, (chunk) => {
        setMessages(prev => {
          const newMessages = [...prev]
          const lastIndex = newMessages.length - 1
          if (newMessages[lastIndex]?.role === 'assistant') {
            newMessages[lastIndex] = {
              ...newMessages[lastIndex],
              content: newMessages[lastIndex].content + chunk
            }
          }
          return newMessages
        })
      })
    } catch (error) {
      console.error('Chat error:', error)
      setMessages(prev => {
        const newMessages = [...prev]
        const lastIndex = newMessages.length - 1
        if (newMessages[lastIndex]?.role === 'assistant') {
          newMessages[lastIndex] = {
            ...newMessages[lastIndex],
            content: '抱歉，发生了错误，请稍后重试。'
          }
        }
        return newMessages
      })
    } finally {
      setIsLoading(false)
    }
  }, [])

  return { messages, sendMessage, isLoading }
}
