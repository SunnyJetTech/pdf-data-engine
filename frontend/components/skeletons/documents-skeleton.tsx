export default function DocumentsSkeleton() {
  return (
    <div className="space-y-2">
      {[...Array(8)].map((_, i) => (
        <div
          key={i}
          className="h-12 bg-muted rounded animate-pulse"
        />
      ))}
    </div>
  );
}