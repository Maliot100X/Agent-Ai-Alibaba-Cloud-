import asyncio
import json
import os
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, Any, List

# Ensure project modules are importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config_manager import ConfigManager

app = FastAPI()

class GatewayOrchestrator:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.active_connections: Dict[str, WebSocket] = {}
        self.adapters: List[Any] = []

    def load_adapters(self):
        """Dynamically loads enabled adapters from config."""
        channels = self.config_manager.get("channels", {})
        
        if channels.get("telegram", {}).get("enabled"):
            print("🦞 Enabling Telegram Adapter...")
            # Import and start telegram adapter here (mocked for now)
            
        if channels.get("slack", {}).get("enabled"):
            print("🦞 Enabling Slack Adapter...")
            # Import and start slack adapter here (mocked for now)

    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_text(json.dumps(message))

orchestrator = GatewayOrchestrator()

@app.on_event("startup")
async def startup_event():
    orchestrator.load_adapters()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = str(len(orchestrator.active_connections) + 1)
    orchestrator.active_connections[client_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Protocol: Connect/Hello-Ok
            if message.get("type") == "connect":
                await websocket.send_text(json.dumps({
                    "type": "hello-ok",
                    "payload": {
                        "version": "1.0.0",
                        "health": "ok",
                        "config": orchestrator.config_manager.config
                    }
                }))
            
            # Protocol: Req/Res
            elif message.get("type") == "req":
                req_id = message.get("id")
                method = message.get("method")
                params = message.get("params", {})
                
                print(f"🦞 Gateway received request {req_id} for method {method}...")
                
                # Model Routing Logic
                primary_model = orchestrator.config_manager.get("agents.defaults.model.primary")
                print(f"🦞 Routing to Model: {primary_model}")
                
                await websocket.send_text(json.dumps({
                    "type": "res",
                    "id": req_id,
                    "ok": True,
                    "payload": {"status": "request_routed", "model": primary_model}
                }))

    except WebSocketDisconnect:
        del orchestrator.active_connections[client_id]
        print(f"Client {client_id} disconnected.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=18789)
