"use client"

import Skeleton
from "react-loading-skeleton"

export default function PageSkeleton() {
  return (
    <div className="space-y-4">
      <Skeleton height={40} />

      <Skeleton height={120} />

      <Skeleton height={120} />
    </div>
  )
}