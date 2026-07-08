"use client"

import { useEffect, useState } from "react"

export default function QuotaPage() {
  const [quota, setQuota] = useState<any>(null)

  useEffect(() => {
    fetchQuota()
  }, [])

  async function fetchQuota() {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/quota`,
      {
        credentials: "include",
      }
    )

    const data = await response.json()

    setQuota(data)
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">
        Usage Quota
      </h1>

      <div className="border rounded-lg p-6">
        <p>
          Uploads Used:
          {quota?.uploads_used}
        </p>

        <p>
          Upload Limit:
          {quota?.uploads_limit}
        </p>

        <p>
          Searches Used:
          {quota?.searches_used}
        </p>

        <p>
          Searches Limit:
          {quota?.searches_limit}
        </p>
      </div>
    </div>
  )
}