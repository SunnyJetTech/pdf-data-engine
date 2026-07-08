"use client"

import { Trash2 } from "lucide-react"

interface Props {
  onDelete: () => void
}

export function DeleteDocumentButton({
  onDelete,
}: Props) {
  return (
    <button
      onClick={onDelete}
      className="p-2 rounded-md hover:bg-red-500/10"
    >
      <Trash2 className="h-4 w-4 text-red-500" />
    </button>
  )
}