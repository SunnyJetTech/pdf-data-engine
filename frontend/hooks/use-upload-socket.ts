"use client";

import { useCallback, useRef } from "react";

type ProgressPayload = {
  progress?: number;
  current_page?: number;
  total_pages?: number;
};

type CompletePayload = {
  document_id?: number;
  filename?: string;
  mongo_collection?: string;
  rows?: number;
  columns?: number;
};

type ErrorPayload = {
  message: string;
};

type Props = {
  onProgress?: (
    data: ProgressPayload
  ) => void;

  onComplete?: (
    data: CompletePayload
  ) => void;

  onError?: (
    data?: ErrorPayload
  ) => void;
};

export function useUploadSocket({onProgress, onComplete, onError,}: Props) {
  const socketRef = useRef<WebSocket | null>(null);

  const connect = useCallback(
    (clientId: string) => {
      if (!clientId) {
        return;
      }

      const baseUrl = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8002";

      const ws = new WebSocket(`${baseUrl}/pdf/progress/${clientId}`);

      socketRef.current = ws;

      ws.onopen = () => {
        console.log(
          "WebSocket connected"
        );
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        console.log("WS MESSAGE", data );

        if (typeof data.progress === "number") {
          onProgress?.(
            data
          );
          return;
        }


        if (data.status === "processing_complete") {
          onProgress?.({
            progress: 100,
          });
          return;
        }

        if (data.status === "saved_to_mongodb") {
          onComplete?.(
            data
          );

          ws.close();
          return;
        }

        if (data.status === "saved_to_excel") {
          onComplete?.(
            data
          );

          ws.close();
          return;
        }

        if (data.status === "error") {
          onError?.({
            message: data.message || "Upload failed",
          });

          ws.close();
        }
      };

      ws.onerror = () => {
        console.error(
          "WebSocket error"
        );

        onError?.({
          message:
            "WebSocket connection failed",
        });
      };

      ws.onclose = () => {
        console.log(
          "WebSocket closed"
        );

        socketRef.current = null;
      };
    },
    [onProgress, onComplete, onError,]
  );

  const disconnect = useCallback(() => {
      socketRef.current?.close();
      socketRef.current = null;
    }, []);

  return {
    connect,
    disconnect,
  };
}