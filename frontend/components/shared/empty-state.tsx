type Props = {
  title: string
  description: string
}

export default function EmptyState({
  title,
  description,
}: Props) {
  return (
    <div className="border rounded-lg p-10 text-center">
      <h2 className="font-semibold">
        {title}
      </h2>

      <p className="text-muted-foreground">
        {description}
      </p>
    </div>
  )
}