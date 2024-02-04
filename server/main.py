import json
import asyncio
import websockets

sockets = {}
states = {}


async def echo(websocket, path):
    async for message in websocket:
        parsed = json.loads(message)
        if parsed["player_id"] not in sockets:
            sockets[parsed["player_id"]] = websocket

        states[parsed["player_id"]] = parsed

        for player_id in sockets.keys():
            socket = sockets[player_id]
            if player_id != parsed["player_id"]:
                await socket.send(json.dumps(states[parsed["player_id"]]))


start_server = websockets.serve(echo, "localhost", 3000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
