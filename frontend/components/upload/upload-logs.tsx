interface Props {
  logs: string[]
}

export function UploadLogs({
  logs,
}: Props) {
  return (
    <div className="h-72 overflow-auto rounded-lg border bg-card p-4 font-mono text-sm">
      {logs.map((log, index) => (
        <div key={index}>
          {log}
        </div>
      ))}
    </div>
  )
}