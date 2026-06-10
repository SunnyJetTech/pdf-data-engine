"use client"

import { useEffect, useState } from "react";
import { pdfWebSocket } from "@/api/websocket.api";
import { ProgressMessage } from "@/types/websocket-types";

export function usePdfProgress (clientId: string) {
    const [progress, setProgress] = useState<ProgressMessage | null>(null)

    useEffect(() => {
        if (!clientId) return 

        pdfWebSocket.connect(clientId, (data) => {setProgress(data)})
        return () => {
            pdfWebSocket.disconnect()
        }
    }, [clientId])

    return progress
}