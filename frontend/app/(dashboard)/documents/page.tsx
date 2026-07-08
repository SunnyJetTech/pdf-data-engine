"use client"

import { useEffect, useMemo, useState } from "react"
import { useRouter } from "next/navigation"
import {getAllDocuments, deleteDocument,} from "@/api/document.api"
import { Documents } from "@/types/api.types"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {Search, RefreshCw, Trash2, Eye, Database,} from "lucide-react"
import { toast } from "sonner"

export default function DocumentsPage() {
  const router = useRouter()

  const [documents, setDocuments] = useState<Documents[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [deletingId, setDeletingId] = useState<number | null>(null)

  async function loadDocuments() {
    setLoading(true)

    try {
      const res = await getAllDocuments()

      if (res.status === "success") {
        setDocuments(res.data || [])
      }
    } catch {
      toast.error("Failed to load documents")
    } finally {
      setLoading(false)
    }
  }

  async function handleDelete(id: number) {
    if (!confirm("Delete this document?")) return

    setDeletingId(id)

    try {
      await deleteDocument(id)

      setDocuments((prev) =>
        prev.filter((d) => d.id !== id)
      )

      toast.success("Document deleted")
    } catch {
      toast.error("Delete failed")
    } finally {
      setDeletingId(null)
    }
  }

  useEffect(() => {
    loadDocuments()
  }, [])

  const filtered = useMemo(() => {
    return documents.filter((d) =>
      d.filename
        .toLowerCase()
        .includes(searchTerm.toLowerCase())
    )
  }, [documents, searchTerm])

  return (
    <div className="space-y-6">
      <div className="flex justify-between">
        <div>
          <h1 className="text-3xl font-bold">
            Documents
          </h1>
          <p className="text-muted-foreground">
            Manage uploaded PDFs
          </p>
        </div>

        <Button onClick={loadDocuments}>
          <RefreshCw className="mr-2 h-4 w-4" />
          Refresh
        </Button>
      </div>

      <div className="relative max-w-md">
        <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />

        <Input
          className="pl-10"
          value={searchTerm}
          onChange={(e) =>
            setSearchTerm(e.target.value)
          }
          placeholder="Search documents..."
        />
      </div>

      <div className="border rounded-lg">
        {loading ? (
          <div className="p-6 text-center">
            Loading...
          </div>
        ) : filtered.length === 0 ? (
          <div className="p-6 text-center">
            No documents found
          </div>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="p-3 text-left">
                  Name
                </th>
                <th className="p-3 text-left">
                  Collection
                </th>
                <th className="p-3 text-left">
                  Rows
                </th>
                <th className="p-3 text-left">
                  Actions
                </th>
              </tr>
            </thead>

            <tbody>
              {filtered.map((doc) => (
                <tr key={doc.id} className="border-b">
                  <td className="p-3">
                    {doc.filename}
                  </td>

                  <td className="p-3 flex items-center gap-2">
                    <Database className="w-4 h-4" />
                    {doc.mongo_collection}
                  </td>

                  <td className="p-3">
                    {doc.rows}
                  </td>

                  <td className="p-3 flex gap-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() =>
                        router.push(
                          `/documents/${doc.id}`
                        )
                      }
                    >
                      <Eye className="w-4 h-4 mr-1" />
                      View
                    </Button>

                    <Button
                      size="sm"
                      variant="destructive"
                      onClick={() =>
                        handleDelete(doc.id)
                      }
                      disabled={
                        deletingId === doc.id
                      }
                    >
                      <Trash2 className="w-4 h-4 mr-1" />
                      {deletingId === doc.id
                        ? "Deleting"
                        : "Delete"}
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}