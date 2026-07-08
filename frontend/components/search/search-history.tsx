"use client"

import { useEffect, useState } from "react"
import apiClient from "@/lib/axios"

type History = {
  id: number
  column_name: string
  operator: string
  search_value: string
}

type Props = {
  onSelect: (item: History) => void
}

export default function SearchHistory({ onSelect }: Props) {
  const [history, setHistory] = useState<History[]>([])

  async function loadHistory() {
    const res = await apiClient.get("/documents/search-history")
    setHistory(res.data.data || [])
  }

  useEffect(() => {
    loadHistory()
  }, [])

  return (
    <div className="border rounded-lg p-3 space-y-2">
      <h2 className="font-semibold">
        Recent Searches
      </h2>

      {history.length === 0 ? (
        <p className="text-sm text-muted-foreground">
          No history yet
        </p>
      ) : (
        history.map((h) => (
          <div
            key={h.id}
            onClick={() => onSelect(h)}
            className="p-2 hover:bg-muted cursor-pointer rounded-md text-sm"
          >
            {h.column_name} {h.operator}{" "}
            {h.search_value}
          </div>
        ))
      )}
    </div>
  )
}