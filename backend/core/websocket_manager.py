from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[client_id] = websocket

    def disconnect(self, client_id: str):
        self.connections.pop(client_id, None)

    async def send_progress(self, client_id: str, current_page: int, total_pages: int):
        websocket = self.connections.get(client_id)

        if websocket:
            await websocket.send_json({
                "type": "progress",
                "current_page": current_page,
                "total_pages": total_pages,
                "percentage": round(current_page * 100 / total_pages, 2)
            })

    async def send_message(self, client_id: str, payload: dict):
        websocket = self.connections.get(client_id)

        if websocket:
            await websocket.send_json(payload)

manager = ConnectionManager()