"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import {getSingleDocument, deleteDocument,} from "@/api/document.api"
import { Documents } from "@/types/api.types"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Database, Trash2, ArrowLeft, Search } from "lucide-react"

export default function DocumentDetailsPage() {
  const params = useParams()
  const router = useRouter()

  const documentId = Number(params.id)
  const [document, setDocument] = useState<Documents | null>(null)
  const [loading, setLoading] = useState(true)
  const [deleting, setDeleting] = useState(false)
  const [previewRows, setPreviewRows] = useState<Record<string, any>[]>([])
  const [headers, setHeaders] = useState<string[]>([])

  async function loadDocument() {
    try {
      setLoading(true)

      const response = await getSingleDocument(documentId)

      if (response.status === "success") {
        const doc = response.data
        setDocument(doc)

        const rows = (doc as any).preview_rows ?? []

        setPreviewRows(rows)

        if (rows.length > 0) {
          setHeaders(Object.keys(rows[0]))
        }
      }
    } finally {
      setLoading(false)
    }
  }

  async function handleDelete() {
    const confirmDelete = window.confirm(
      "Delete this document permanently?"
    )

    if (!confirmDelete) return

    try {
      setDeleting(true)

      const response = await deleteDocument(documentId)

      if (response.status === "success") {
        router.push("/dashboard/documents")
      }
    } finally {
      setDeleting(false)
    }
  }

  useEffect(() => {
    if (documentId) {
      loadDocument()
    }
  }, [documentId])

  if (loading) {
    return <div className="p-6">Loading document...</div>
  }

  if (!document) {
    return <div className="p-6">Document not found</div>
  }

  return (
    <div className="space-y-6">

      <div className="flex items-center justify-between">
        <div>
          <Button
            variant="ghost"
            onClick={() => router.back()}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>

          <h1 className="text-3xl font-bold mt-2">
            {document.filename}
          </h1>

          <p className="text-muted-foreground">
            Dataset Explorer
          </p>
        </div>

        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={() =>
              router.push(
                `/search?documentId=${document.id}`
              )
            }
          >
            <Search className="h-4 w-4 mr-2" />
            Search
          </Button>

          <Button
            variant="destructive"
            onClick={handleDelete}
            disabled={deleting}
          >
            <Trash2 className="h-4 w-4 mr-2" />
            {deleting ? "Deleting..." : "Delete"}
          </Button>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="p-5">
            <div className="text-sm text-muted-foreground">
              Collection
            </div>
            <div className="flex items-center gap-2 mt-2">
              <Database className="h-4 w-4" />
              <span className="font-medium">
                {document.mongo_collection}
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-5">
            <div className="text-sm text-muted-foreground">
              Rows
            </div>
            <div className="text-2xl font-bold mt-2">
              {document.rows.toLocaleString()}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-5">
            <div className="text-sm text-muted-foreground">
              Columns
            </div>
            <div className="text-2xl font-bold mt-2">
              {document.columns}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Columns</CardTitle>
        </CardHeader>

        <CardContent>
          {headers.length === 0 ? (
            <p className="text-muted-foreground">
              No preview data available
            </p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {headers.map((col) => (
                <span
                  key={col}
                  className="px-3 py-1 border rounded-md text-sm"
                >
                  {col}
                </span>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Preview Data</CardTitle>
        </CardHeader>

        <CardContent>
          {previewRows.length === 0 ? (
            <p className="text-muted-foreground">
              No preview rows available
            </p>
          ) : (
            <div className="overflow-auto">
              <table className="w-full border">
                <thead>
                  <tr>
                    {headers.map((h) => (
                      <th
                        key={h}
                        className="border p-2 text-left"
                      >
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>

                <tbody>
                  {previewRows.map((row, i) => (
                    <tr key={i}>
                      {headers.map((h) => (
                        <td
                          key={h}
                          className="border p-2"
                        >
                          {row[h]}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

    </div>
  )
}