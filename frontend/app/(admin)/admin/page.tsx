"use client"

import { useEffect, useState } from "react"
import {
  getDashboardStats,
  getRevenueAnalytics,
} from "@/api/admin.api"

import RevenueChart from "@/components/admin/revenue-chart"

export default function AdminDashboard() {
  const [stats, setStats] = useState<any>(null)

  const [revenue, setRevenue] =
    useState<any[]>([])

  const [loading, setLoading] =
    useState(true)

  useEffect(() => {
    load()
  }, [])

  async function load() {
    try {
      const [
        statsResponse,
        revenueResponse,
      ] = await Promise.all([
        getDashboardStats(),
        getRevenueAnalytics(),
      ])

      if (
        statsResponse.status === "success"
      ) {
        setStats(statsResponse.data)
      }

      setRevenue(
        revenueResponse.data || []
      )
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="p-6">
        Loading dashboard...
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">
        Admin Dashboard
      </h1>

      <div className="grid md:grid-cols-4 gap-4">
        <div className="border rounded-lg p-5">
          <p>Total Users</p>

          <h2 className="text-3xl font-bold">
            {stats?.users ?? 0}
          </h2>
        </div>

        <div className="border rounded-lg p-5">
          <p>Documents</p>

          <h2 className="text-3xl font-bold">
            {stats?.documents ?? 0}
          </h2>
        </div>

        <div className="border rounded-lg p-5">
          <p>Searches</p>

          <h2 className="text-3xl font-bold">
            {stats?.searches ?? 0}
          </h2>
        </div>

        <div className="border rounded-lg p-5">
          <p>Revenue</p>

          <h2 className="text-3xl font-bold">
            ₦{stats?.revenue ?? 0}
          </h2>
        </div>
      </div>

      <RevenueChart
        data={revenue}
      />
    </div>
  )
}