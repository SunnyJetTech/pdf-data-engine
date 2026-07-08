interface Props {
  progress: number
}

export function UploadProgress({
  progress,
}: Props) {
  return (
    <div className="space-y-2">
      <div className="h-3 w-full overflow-hidden rounded-full bg-muted">
        <div
          className="h-full bg-primary transition-all duration-300"
          style={{
            width: `${progress}%`,
          }}
        />
      </div>

      <div className="text-sm text-muted-foreground">
        {progress.toFixed(0)}%
      </div>
    </div>
  )
}