from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List
from fastapi.security.utils import get_authorization_scheme_param

app = FastAPI()

# Define a directory for static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

async def get_current_user(websocket: WebSocket):
    auth_header = websocket.headers.get('Authorization')
    if auth_header is None:
        raise HTTPException(status_code=403, detail="Authorization header missing")

    scheme, token = get_authorization_scheme_param(auth_header)
    if scheme.lower() != "bearer" or token != "valid_token":  # Replace 'valid_token' with actual token validation
        raise HTTPException(status_code=403, detail="Invalid token")

    return token  # or return user data if using a more complex auth system

@app.get("/")
async def get():
    # Redirect to static HTML file
    return HTMLResponse(content=open("static/study3.html", "r", encoding="utf-8").read(), status_code=200)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    # Authenticate user
    await get_current_user(websocket)
    
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} left the chat")
