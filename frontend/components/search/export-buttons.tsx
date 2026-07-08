"use client"

import { Button } from "@/components/ui/button"
import { exportCsv, exportExcel } from "@/api/export.api"
import { toast } from "sonner"

type Props = {
  payload: any
}

export default function ExportButtons({ payload }: Props) {
  async function handleExport(type: "csv" | "excel") {
    try {
      const res =
        type === "csv"
          ? await exportCsv(payload)
          : await exportExcel(payload)

      const blob = new Blob([res], {
        type:
          type === "csv"
            ? "text/csv"
            : "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      })

      const url = window.URL.createObjectURL(blob)

      const a = document.createElement("a")
      a.href = url
      a.download =
        type === "csv"
          ? "export.csv"
          : "export.xlsx"

      a.click()

      toast.success("Export completed")
    } catch {
      toast.error("Export failed")
    }
  }

  return (
    <div className="flex gap-2">
      <Button
        variant="outline"
        onClick={() => handleExport("csv")}
      >
        Export CSV
      </Button>

      <Button
        variant="outline"
        onClick={() => handleExport("excel")}
      >
        Export Excel
      </Button>
    </div>
  )
}