import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
import json

from dotenv import dotenv_values
from typing import List, Dict
from api.temperature import post_temperature as api_post_temperature
from api.temperature import get_temperatures as api_get_temperatures
from api.temperature import get_pseudo_tables as api_get_pseudo_tables
from api.temperature import remove_pseudo_table
from api.temperature import construct_excel

from api.settings import set_item as api_set_item

from models.TemperaturePostModel import TemperaturePostModel
from models.Success import Success
from models.SetSettingModel import SetSettingModel

from api.settings import get_settings

config = dotenv_values(".env")
app = FastAPI(debug=config.get("DEBUG"))

app.mount("/static", StaticFiles(directory="static"), name="static")


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()
manager1 = ConnectionManager()

def file_get_contents(path: str) -> str:
    with open(path) as fr:
        content = fr.read()
        return content

@app.post("/api/temperature", response_model=Success)
async def post_temperature(request: TemperaturePostModel):
    await manager1.broadcast(json.dumps({
        'event': 'data_updated',
        'temperature': request.dict()
    }))
    return api_post_temperature(request)

@app.get("/api/temperatures/{pseudo_table_id}")
def get_pseudo_tables_temperatures(pseudo_table_id: str):
    return api_get_temperatures(pseudo_table_id)

@app.delete("/api/temperatures/{pseudo_table_id}")
def delete_pseudo_table(pseudo_table_id: str):
    return remove_pseudo_table(pseudo_table_id)

@app.post("/api/send_reboot")
async def send_reboot():
    await manager.broadcast(json.dumps({
        'event': 'reboot'
    }))
    return Success(success=True)

@app.get("/api/pseudo_tables")
def get_pseudo_tables_ids():
    return api_get_pseudo_tables()

@app.post("/api/settings")
async def set_setting(request: SetSettingModel):
    result = api_set_item(request.k, request.v)
    await manager.broadcast(json.dumps({
        'event': 'setting_changed',
        'setting_key': request.k,
        'setting_value': request.v
    }))
    return result

@app.get("/api/settings")
def get_settings_() -> Dict[str, str]:
    return get_settings()

@app.get("/", response_class=HTMLResponse)
def get_main_page():
    base = file_get_contents("base.html")
    navbar = file_get_contents("navbar.html")
    index = file_get_contents("index.html")

    html = base.replace("<Navbar />", navbar)
    html = html.replace("<Content />", index)
    return HTMLResponse(html)

@app.get("/{pseudo_table_id}.xlsx", response_class=StreamingResponse)
def generate_excel_workbook(pseudo_table_id: str):
    final_filename = construct_excel(pseudo_table_id)
    def iterfile():
        with open(final_filename, mode="rb") as file_like:
            yield from file_like
        os.unlink(final_filename)
    resp = StreamingResponse(iterfile(), media_type="octet/stream")
    return resp

@app.websocket("/ws/settings")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.websocket("/ws/charts")
async def websocket_endpoint(websocket: WebSocket):
    await manager1.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager1.disconnect(websocket)