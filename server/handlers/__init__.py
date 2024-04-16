sockets = {}
states = {}
rooms = {}
player_room = {}

def update_state(username, state):
    states[username] = state
    states[username]["username"] = username

    if username in player_room:
        room_id = player_room[username]
        for player_id in rooms[room_id]:
            if player_id != username:
                yield states[username], sockets[player_id] 


def connect(username, room_id, sid):
    player_id = username
    sockets[player_id] = sid

    if room_id not in rooms:
        rooms[room_id] = []
    if len(rooms[room_id]) < 2:
        rooms[room_id].append(player_id)
        player_room[player_id] = room_id

    for player_id in rooms[room_id]:
        if player_id != username:
            yield states[player_id], sockets[username]
