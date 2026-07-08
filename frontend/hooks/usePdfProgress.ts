"use client"

import { useEffect, useState } from "react"
import { ProgressSocket } from "@/lib/websocket"

export function usePdfProgress(
  clientId: string
) {
  const [progress, setProgress] = useState<any>(null)

  useEffect(() => {
    const ws = new ProgressSocket()

    ws.connect(clientId, (message) => {
        setProgress(message)
      }
    )

    return () => {ws.disconnect()}
  }, [clientId])

  return progress
}