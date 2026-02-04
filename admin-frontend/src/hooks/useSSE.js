import { useEffect, useRef, useCallback } from 'react'

const API_URL = import.meta.env.VITE_API_URL || '/api/v1'

export function useSSE(onEvent) {
  const reconnectTimeoutRef = useRef(null)
  const abortControllerRef = useRef(null)

  const connect = useCallback(() => {
    const token = localStorage.getItem('admin_token')
    if (!token) return

    // 기존 연결 정리
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    abortControllerRef.current = new AbortController()
    const url = `${API_URL}/admin/orders/stream`

    const fetchSSE = async () => {
      try {
        const response = await fetch(url, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          signal: abortControllerRef.current.signal,
        })

        if (!response.ok) {
          throw new Error('SSE connection failed')
        }

        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ''

        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop() || ''

          let eventType = null
          let eventData = null

          for (const line of lines) {
            if (line.startsWith('event:')) {
              eventType = line.slice(6).trim()
            } else if (line.startsWith('data:')) {
              try {
                eventData = JSON.parse(line.slice(5).trim())
              } catch {
                eventData = line.slice(5).trim()
              }
            } else if (line === '' && eventType && eventData !== null) {
              onEvent({ type: eventType, data: eventData })
              eventType = null
              eventData = null
            }
          }
        }
      } catch (error) {
        if (error.name !== 'AbortError') {
          console.error('SSE error:', error)
          reconnectTimeoutRef.current = setTimeout(connect, 5000)
        }
      }
    }

    fetchSSE()
  }, [onEvent])

  const disconnect = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
      reconnectTimeoutRef.current = null
    }
  }, [])

  useEffect(() => {
    connect()
    return () => disconnect()
  }, [connect, disconnect])

  return { connect, disconnect }
}
