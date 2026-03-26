import asyncio
import json
import uuid
import websockets
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAdapter(ABC):
    def __init__(self, gateway_url: str = "ws://localhost:18789/ws"):
        self.gateway_url = gateway_url
        self.active_requests: Dict[str, Any] = {}

    async def connect_to_gateway(self):
        """Initializes a WebSocket connection to the Gateway."""
        async with websockets.connect(self.gateway_url) as websocket:
            # Handshake
            await websocket.send(json.dumps({"type": "connect"}))
            response = await websocket.recv()
            hello_ok = json.loads(response)
            if hello_ok.get("type") == "hello-ok":
                print("✓ Successfully connected to AccioClaw Gateway.")
                return websocket
            else:
                raise Exception("! Handshake failed.")

    async def send_to_gateway(self, text: str, platform: str, user_id: str, channel_id: str):
        """Normalizes and sends a message to the Gateway."""
        req_id = str(uuid.uuid4())
        request = {
            "type": "req",
            "id": req_id,
            "method": "process_message",
            "params": {
                "text": text,
                "platform": platform,
                "user_id": user_id,
                "channel_id": channel_id
            }
        }
        
        async with websockets.connect(self.gateway_url) as websocket:
            await websocket.send(json.dumps({"type": "connect"}))
            await websocket.recv() # hello-ok
            
            await websocket.send(json.dumps(request))
            response = await websocket.recv()
            data = json.loads(response)
            return data.get("payload", {})

    @abstractmethod
    async def start(self):
        """Starts the adapter listening on its platform."""
        pass
