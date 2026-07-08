from typing import Any
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:

    def __init__(self):
        self.connections: dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket,) -> None:
        await websocket.accept()
        self.connections[client_id] = websocket

    def disconnect(self, client_id: str) -> None:
        self.connections.pop(client_id, None)

    def is_connected(self, client_id: str) -> bool:
        return client_id in self.connections

    async def send(self, client_id: str, payload: dict[str, Any]) -> bool:
        websocket = self.connections.get(client_id)

        if websocket is None:
            return False

        try:
            await websocket.send_json(payload)
            return True

        except Exception:
            self.disconnect(client_id)
            return False

    async def send_progress(self, client_id: str, current_page: int, total_pages: int) -> bool:
        percentage = 0

        if total_pages > 0:
            percentage = round(current_page * 100 / total_pages, 2)

        return await self.send(
            client_id,
            {
                "type": "progress",
                "current_page": current_page,
                "total_pages": total_pages,
                "percentage": percentage,
            },
        )

    async def broadcast(self, payload: dict[str, Any]) -> None:
        disconnected = []

        for client_id, websocket in self.connections.items():

            try:
                await websocket.send_json(payload)

            except Exception:
                disconnected.append(client_id)

        for client_id in disconnected:
            self.disconnect(client_id)

    async def close(self, client_id: str) -> None:
        websocket = self.connections.get(client_id)

        if websocket:

            await websocket.close()

            self.disconnect(client_id)

    @property
    def active_connections(self) -> int:
        return len(self.connections)


manager = ConnectionManager()