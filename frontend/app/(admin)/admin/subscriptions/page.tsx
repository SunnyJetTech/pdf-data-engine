"use client"

import { useEffect, useState } from "react"
import {getSubscriptions,} from "@/api/admin.api"

export default function SubscriptionsPage() {
  const [items, setItems] = useState<any[]>([])

  useEffect(() => {
    getSubscriptions().then((res) => {
      setItems(res.data || [])
    })
  }, [])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">
        Subscriptions
      </h1>

      <table className="w-full border">
        <thead>
          <tr>
            <th>User</th>
            <th>Plan</th>
            <th>Status</th>
            <th>Expires</th>
          </tr>
        </thead>

        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.user_id}</td>
              <td>{item.plan}</td>
              <td>{item.status}</td>
              <td>{item.expires_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}