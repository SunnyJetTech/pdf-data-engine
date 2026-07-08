interface Props {
  rows: number
  columns: number
  collection?: string
}

export function UploadSummary({
    rows,
  columns,
  collection,
}: Props) {
  return (
    <div className="rounded-lg border bg-card p-5">
      <h3 className="font-semibold">
        Upload Complete
      </h3>

      <div className="mt-4 grid gap-4 md:grid-cols-3">
        <div>
          <p className="text-muted-foreground text-sm">
            Rows
          </p>

          <p className="text-2xl font-bold">
            {rows.toLocaleString()}
          </p>
        </div>

        <div>
          <p className="text-muted-foreground text-sm">
            Columns
          </p>

          <p className="text-2xl font-bold">
            {columns}
          </p>
        </div>

        <div>
          <p className="text-muted-foreground text-sm">
            Collection
          </p>

          <p className="font-medium break-all">
            {collection}
          </p>
        </div>
      </div>
    </div>
  )
}