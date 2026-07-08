type WSMessage = {
  status?: string;
  type?: string;
  [key: string]: any;
};

class WSManager {
  private socket: WebSocket | null = null;

  private reconnectTimer:
    | NodeJS.Timeout
    | null = null;

  private url: string | null = null;

  private listeners = new Map<string, (data: any) => void>();

  connect(url: string) {
    if (
      this.socket &&
      (
        this.socket.readyState === WebSocket.OPEN ||
        this.socket.readyState === WebSocket.CONNECTING
      )
    ) {
      return;
    }

    this.url = url;

    this.socket = new WebSocket(url);

    this.socket.onopen = () => {
      console.log(
        "WebSocket connected"
      );
    };

    this.socket.onmessage = (
      event
    ) => {
      try {
        const data: WSMessage = JSON.parse(event.data);

        console.log("WS MESSAGE:", data);

        const eventKey = data.type || data.status;

        if (!eventKey) {
          return;
        }

        const handler = this.listeners.get(eventKey);

        if (handler) {
          handler(data);
        }
      } catch (error) {
        console.error("Invalid websocket message", error);
      }
    };

    this.socket.onclose = (event) => {
      console.log("WebSocket disconnected", event.code, event.reason);

      this.reconnect();
    };

    this.socket.onerror = (error) => {console.error("WebSocket error", error);
    };
  }

  private reconnect() {
    if (!this.url) {
      return;
    }

    if (this.reconnectTimer) {
      clearTimeout(
        this.reconnectTimer
      );
    }

    this.reconnectTimer =
      setTimeout(() => {
        console.log(
          "Attempting websocket reconnect..."
        );

        this.connect(
          this.url!
        );
      }, 2000);
  }

  subscribe(
    event: string,
    callback: (
      data: any
    ) => void
  ) {
    this.listeners.set(
      event,
      callback
    );
  }

  unsubscribe(event: string) {
    this.listeners.delete(
      event
    );
  }

  disconnect() {
    if (
      this.reconnectTimer
    ) {
      clearTimeout(
        this.reconnectTimer
      );
    }

    if (this.socket) {
      this.socket.close();
    }

    this.socket = null;
  }
}

export const wsManager = new WSManager();