export default function UsersSkeleton() {
  return (
    <div className="space-y-2">
      {[...Array(6)].map((_, i) => (
        <div
          key={i}
          className="h-14 bg-muted rounded animate-pulse"
        />
      ))}
    </div>
  );
}