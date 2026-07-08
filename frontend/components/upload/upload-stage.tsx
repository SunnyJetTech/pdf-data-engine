import {CheckCircle2, Loader2, Circle,} from "lucide-react"

interface Props {
  currentStage: string
}

const stages = [
  "uploading",
  "processing",
  "saving",
  "completed",
]

export function UploadStage({
  currentStage,
}: Props) {
  const currentIndex = stages.indexOf(currentStage)

  return (
    <div className="space-y-3">
      {stages.map((stage, index) => {
        const completed = index < currentIndex

        const active = index === currentIndex

        return (
          <div key={stage} className="flex items-center gap-3">
            {completed ? (
              <CheckCircle2 className="h-5 w-5 text-green-500" />
            ) : active ? (
              <Loader2 className="h-5 w-5 animate-spin text-primary" />
            ) : (
              <Circle className="h-5 w-5 text-muted-foreground" />
            )}

            <span className="capitalize"> {stage} </span>
          </div>
        )
      })}
    </div>
  )
}