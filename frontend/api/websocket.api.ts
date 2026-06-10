import { ProgressMessage } from "@/types/websocket-types";

export class PDFWebsocket {
    private socket: WebSocket | null = null

    connect(clientId: string, onMessage: (data: ProgressMessage) => void) {
        const baseUrl = process.env.NEXT_PUBLIC_WS_URL

        this.socket = new WebSocket(`${baseUrl}/pdf/progress/${clientId}`)
        this.socket.onopen = () => {
            console.log("Websocket Connected")
        }

        this.socket.onmessage = (event) => {
            const data: ProgressMessage = JSON.parse(event.data)

            onMessage(data)
        }

        this.socket.onerror = (error) => {
            console.log(error)
        }

        this.socket.onclose = (error) => {
            console.log(error)
        }
    }

    disconnect() {
        this.socket?.close()
    }
}

export const pdfWebSocket = new PDFWebsocket()