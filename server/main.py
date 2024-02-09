import json
import asyncio
import websockets

sockets = {}
states = {}
rooms = {}
player_room = {}

async def echo(websocket, path):
    async for message in websocket:
        parsed = json.loads(message)
        if parsed["type"] == "update_state":
            states[parsed["player_id"]] = parsed

            for player_id in rooms[player_room[parsed["player_id"]]]:
                socket = sockets[player_id]
                if player_id != parsed["player_id"]:
                    await socket.send(json.dumps(states[parsed["player_id"]]))
        
        elif parsed["type"] == "connect":
            sockets[parsed["player_id"]] = websocket
            if parsed["room_id"] not in rooms:
                rooms[parsed["room_id"]] = []
            if len(rooms[parsed["room_id"]]) < 2:
                rooms[parsed["room_id"]].append(parsed["player_id"])
                player_room[parsed["player_id"]] = parsed["room_id"]


start_server = websockets.serve(echo, "0.0.0.0", 3000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
