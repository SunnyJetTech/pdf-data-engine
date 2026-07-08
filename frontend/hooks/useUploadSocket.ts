import { useCallback, useRef } from "react"

type Props = {
  onProgress?: (data: any) => void
  onComplete?: (data: any) => void
  onError?: () => void
}

export function useUploadSocket({onProgress, onComplete, onError}: Props) {
  const socketRef = useRef<WebSocket | null>(null)

  const connect = useCallback((uploadId: string) => {
    const ws = new WebSocket(`${process.env.NEXT_PUBLIC_WS_URL}/upload/${uploadId}`)

    socketRef.current = ws

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)

      switch (data.type) {
        case "progress":
          onProgress?.(data)
          break

        case "completed":
          onComplete?.(data)
          ws.close()
          break

        case "error":
          onError?.()
          ws.close()
          break
      }
    }

    ws.onerror = () => {
      onError?.()
    }
  }, [])

  return { connect }
}