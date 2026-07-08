"use client"

import { useDropzone } from "react-dropzone"
import { UploadCloud } from "lucide-react"

interface Props {
  onFileSelect: (
    file: File
  ) => void
}

export function UploadDropzone({
  onFileSelect,
}: Props) {
  const { getRootProps, getInputProps } =
    useDropzone({
      accept: {
        "application/pdf": [".pdf"],
      },

      multiple: false,

      onDrop(files) {
        if (files[0]) {
          onFileSelect(files[0])
        }
      },
    })

  return (
    <div
      {...getRootProps()}
      className="
      border-2
      border-dashed
      rounded-xl
      p-12
      text-center
      cursor-pointer
      hover:border-primary
      transition
      "
    >
      <input {...getInputProps()} />

      <UploadCloud className="mx-auto h-12 w-12 mb-4 text-primary" />

      <h3 className="font-semibold text-lg">
        Upload PDF
      </h3>

      <p className="text-muted-foreground">
        Drag & drop PDF here or click
      </p>
    </div>
  )
}