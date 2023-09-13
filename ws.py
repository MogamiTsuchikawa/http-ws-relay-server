import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    global connected_clients
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast received message to all connected clients
            await asyncio.wait([client.send(message) for client in connected_clients])
    finally:
        connected_clients.remove(websocket)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    server = websockets.serve(handler, '0.0.0.0', 3000)
    loop.run_until_complete(server)
    loop.run_forever()
