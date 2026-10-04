import { ProgressMessage } from "@/types/websocket-types";

class PDFWebSocket {

  private socket: WebSocket | null = null;

  connect(clientId: string, onMessage: (message: ProgressMessage) => void) {

    if (this.socket) {this.socket.close();}

    const base = process.env.NEXT_PUBLIC_WS_URL;

    this.socket = new WebSocket(`${base}/api/v1/pdf/progress/${clientId}`);

    this.socket.onopen = () => console.log("WebSocket connected");

    this.socket.onmessage = (event) => onMessage(JSON.parse(event.data));

    this.socket.onerror = console.error;

    this.socket.onclose = () => console.log("WebSocket disconnected");}

  disconnect() { this.socket?.close(); this.socket = null;}
}

export const pdfWebSocket = new PDFWebSocket();