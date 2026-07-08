export default function Loading() {
  return (
    <div className="p-10 space-y-3">
      <div className="h-6 w-1/3 bg-muted animate-pulse rounded" />
      <div className="h-4 w-1/2 bg-muted animate-pulse rounded" />
      <div className="h-4 w-2/3 bg-muted animate-pulse rounded" />
    </div>
  )
}