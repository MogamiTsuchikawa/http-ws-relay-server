import aiohttp
from aiohttp import web
import websockets
import asyncio
import json

# Websocket clients
ws_clients = set()

# HTTP Handler for JSON
async def handle_json(request):
    data = await request.json()
    peername = request.transport.get_extra_info('peername')
    if peername is not None:
        host, port = peername
        data['ClientIp'] = host
    print(data)
    for ws in ws_clients:
        await ws.send_json(data)
    return web.Response()

# WebSocket Handler
async def handle_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    ws_clients.add(ws)
    try:
        async for msg in ws:
            pass
    finally:
        ws_clients.remove(ws)

    return ws

# Routes
app = web.Application()
app.add_routes([web.post('/', handle_json),
                web.get('/ws', handle_websocket)])

# Run the server
web.run_app(app, host='tsuchikawa-raspi.local', port=8080)
