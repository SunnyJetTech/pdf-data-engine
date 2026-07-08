"use client"

import { useEffect, useState } from "react"

export function useUploadProgress(
  clientId: string | null
) {
  const [progress, setProgress] = useState(0)

  const [currentPage, setCurrentPage] =
    useState(0)

  const [totalPages, setTotalPages] =
    useState(0)

  const [logs, setLogs] = useState<string[]>([])

  const [status, setStatus] =
    useState("waiting")

  useEffect(() => {
    if (!clientId) return

    const ws = new WebSocket(
      `${process.env.NEXT_PUBLIC_WS_URL}/pdf/progress/${clientId}`
    )

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if (data.type === "progress") {
        setProgress(data.percentage)

        setCurrentPage(
          data.current_page
        )

        setTotalPages(
          data.total_pages
        )

        setLogs((prev) => [
          ...prev,
          `Processing page ${data.current_page}/${data.total_pages}`,
        ])
      }

      if (data.status) {
        setStatus(data.status)

        setLogs((prev) => [
          ...prev,
          data.status,
        ])
      }
    }

    return () => {
      ws.close()
    }
  }, [clientId])

  return {
    progress,
    currentPage,
    totalPages,
    logs,
    status,
  }
}