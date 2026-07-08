"use client"

import { useEffect, useMemo, useState } from "react"
import { getAllDocuments, SearchColumn, SearchDocument,} from "@/api/document.api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import ExportButtons from "@/components/search/export-buttons"
import SearchHistory from "@/components/search/search-history"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue, } from "@/components/ui/select"

type Row = Record<string, any>

export default function SearchPage() {
  const [documents, setDocuments] = useState<any[]>([])
  const [columns, setColumns] = useState<string[]>([])
  const [documentId, setDocumentId] = useState<number | null>(null)
  const [column, setColumn] = useState("")
  const [operator, setOperator] = useState("=")
  const [value, setValue] = useState("")
  const [results, setResults] = useState<Row[]>([])
  const [loadingDocuments, setLoadingDocuments] = useState(true)
  const [loadingColumns, setLoadingColumns] = useState(false)
  const [loadingSearch, setLoadingSearch] = useState(false)

  useEffect(() => {
    async function loadDocuments() {
      try {
        setLoadingDocuments(true)

        const response = await getAllDocuments()

        console.log(
          "Documents:",
          response.data
        )

        setDocuments(response.data ?? [])
      } catch (error) {
        console.error(
          "Failed loading documents",
          error
        )
      } finally {
        setLoadingDocuments(false)
      }
    }

    loadDocuments()
  }, [])


  useEffect(() => {
    if (!documentId) return

    async function loadColumns() {
      try {
        setLoadingColumns(true)

        const response = SearchColumn(documentId)

        console.log(
          "Columns:",
          response.data
        )

        const cols = response.data ?? []

        setColumns(cols)

        if (cols.length > 0) {
          setColumn(cols[0])
        } else {
          setColumn("")
        }
      } catch (error) {
        console.error(
          "Failed loading columns",
          error
        )

        setColumns([])
        setColumn("")
      } finally {
        setLoadingColumns(false)
      }
    }

    loadColumns()
  }, [documentId])

  const payload = useMemo(
    () => ({
      document_id: documentId,
      column,
      operator,
      value,
    }),
    [
      documentId,
      column,
      operator,
      value,
    ]
  )

  async function handleSearch() {
    if (
      !documentId ||
      !column ||
      !value.trim()
    )
      return

    try {
      setLoadingSearch(true)

      const response = await SearchDocument({document_id: documentId,column, operator, value,})

      console.log(
        "Search response:",
        response
      )

      setResults(
        response.data.results ?? []
      )
    } catch (error) {
      console.error(error)
      setResults([])
    } finally {
      setLoadingSearch(false)
    }
  }

  const headers = useMemo(() => {
    if (!results.length) return []

    return Object.keys(results[0])
  }, [results])

  return (
    <div className="grid grid-cols-12 gap-6">

      <div className="col-span-9 space-y-6">

        <h1 className="text-3xl font-bold">
          Search Dataset
        </h1>

        {/* Document */}

        <Select
          value={
            documentId
              ? documentId.toString()
              : ""
          }
          onValueChange={(value) => {
            const id = Number(value)

            setDocumentId(id)

            setColumns([])
            setColumn("")
            setValue("")
            setResults([])
          }}
        >
          <SelectTrigger>
            <SelectValue
              placeholder={
                loadingDocuments
                  ? "Loading documents..."
                  : "Select Document"
              }
            />
          </SelectTrigger>

          <SelectContent>
            {documents.map((doc) => (
              <SelectItem
                key={doc.id}
                value={doc.id.toString()}
              >
                {doc.filename}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {/* Column */}

        <Select
          value={column}
          onValueChange={setColumn}
          disabled={
            !documentId ||
            loadingColumns ||
            !columns.length
          }
        >
          <SelectTrigger>
            <SelectValue
              placeholder={
                loadingColumns
                  ? "Loading columns..."
                  : "Select Column"
              }
            />
          </SelectTrigger>

          <SelectContent>
            {columns.map((col) => (
              <SelectItem
                key={col}
                value={col}
              >
                {col}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {/* Operator */}

        <Select
          value={operator}
          onValueChange={setOperator}
        >
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>

          <SelectContent>
            {[
              "=",
              "contains",
              "startswith",
              "endswith",
              ">",
              "<",
              ">=",
              "<=",
            ].map((op) => (
              <SelectItem
                key={op}
                value={op}
              >
                {op}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {/* Value */}

        <Input
          placeholder="Enter search value"
          value={value}
          onChange={(e) =>
            setValue(e.target.value)
          }
        />

        <Button
          onClick={handleSearch}
          disabled={
            loadingSearch ||
            !documentId ||
            !column ||
            !value.trim()
          }
        >
          {loadingSearch
            ? "Searching..."
            : "Search"}
        </Button>

        <ExportButtons payload={payload} />

        {/* Results */}

        <div className="rounded-lg border overflow-auto">

          {!results.length ? (
            <div className="p-8 text-center text-muted-foreground">
              No results
            </div>
          ) : (
            <table className="min-w-full">

              <thead>

                <tr>
                  {headers.map((header) => (
                    <th
                      key={header}
                      className="border-b p-3 text-left font-medium"
                    >
                      {header}
                    </th>
                  ))}
                </tr>

              </thead>

              <tbody>

                {results.map(
                  (row, index) => (
                    <tr
                      key={index}
                      className="border-b"
                    >
                      {headers.map(
                        (header) => (
                          <td
                            key={header}
                            className="p-3"
                          >
                            {String(
                              row[header]
                            )}
                          </td>
                        )
                      )}
                    </tr>
                  )
                )}

              </tbody>

            </table>
          )}

        </div>

      </div>

      <div className="col-span-3">

        <SearchHistory
          onSelect={(history) => {
            setColumn(
              history.column_name
            )

            setOperator(
              history.operator
            )

            setValue(
              history.search_value
            )
          }}
        />

      </div>

    </div>
  )
}