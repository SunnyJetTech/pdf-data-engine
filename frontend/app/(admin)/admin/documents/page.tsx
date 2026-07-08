"use client"

import { useEffect, useState } from "react"
import { adminApi } from "@/api/admin.api"

export default function AdminDocumentsPage() {
const [documents, setDocuments] = useState([])

useEffect(() => {
adminApi.documents().then(setDocuments)
}, [])

async function remove(id:number) {
if (!confirm("Delete document?"))
return

```
await adminApi.deleteDocument(id)

setDocuments(prev =>
  prev.filter((d:any) => d.id !== id)
)
```

}

return ( <div> <h1 className="text-3xl font-bold mb-6">
Documents </h1>

```
  <table className="w-full border">
    <thead>
      <tr>
        <th>Filename</th>
        <th>Owner</th>
        <th>Rows</th>
        <th />
      </tr>
    </thead>

    <tbody>
      {documents.map((doc:any) => (
        <tr key={doc.id}>
          <td>{doc.filename}</td>
          <td>{doc.owner_email}</td>
          <td>{doc.rows}</td>

          <td>
            <button
              onClick={() =>
                remove(doc.id)
              }
            >
              Delete
            </button>
          </td>
        </tr>
      ))}
    </tbody>
  </table>
</div>
```

)
}
