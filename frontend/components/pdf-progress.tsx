"use client"

import { usePdfProgress } from "@/hooks/use-pdf-progress"

interface Props {
    clientId: string
}

export default function PdfProgress ({
    clientId,
} : Props) {
    const progress = usePdfProgress(clientId)

    if (!progress) {
        return null
    }

    return (
        <div>
            <p>Processing PDF</p>

            <p>
                {progress.current_page}/{progress.total_pages}
            </p>

            <p>{progress.percentage}</p>

            {progress.message && (
                <p>{progress.message}</p>
            )}
        </div>
    )
}