"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"

type Condition = {
  column: string
  operator: string
  value: string
}

export default function SearchBuilder({
  columns,
  onSearch,
}: {
  columns: string[]
  onSearch: (conditions: Condition[]) => void
}) {
  const [conditions, setConditions] = useState<Condition[]>([
    { column: "", operator: "=", value: "" },
  ])

  function update(index: number, key: string, value: string) {
    const copy = [...conditions]
    copy[index][key] = value
    setConditions(copy)
  }

  function addCondition() {
    setConditions([
      ...conditions,
      { column: "", operator: "=", value: "" },
    ])
  }

  return (
    <div className="space-y-4 border p-4 rounded-lg">
      {conditions.map((c, i) => (
        <div key={i} className="flex gap-2">
          <select
            onChange={(e) =>
              update(i, "column", e.target.value)
            }
          >
            {columns.map((col) => (
              <option key={col}>{col}</option>
            ))}
          </select>

          <select
            onChange={(e) =>
              update(i, "operator", e.target.value)
            }
          >
            <option>=</option>
            <option>contains</option>
            <option>&gt;</option>
            <option>&lt;</option>
          </select>

          <input
            className="border px-2"
            onChange={(e) =>
              update(i, "value", e.target.value)
            }
          />
        </div>
      ))}

      <div className="flex gap-2">
        <Button onClick={addCondition}>
          Add Filter
        </Button>

        <Button onClick={() => onSearch(conditions)}>
          Run Search
        </Button>
      </div>
    </div>
  )
}