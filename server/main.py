from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

sockets = {}
states = {}
rooms = {}
player_room = {}


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("message")
def handle_message(data):
    if "username" not in session:
        return

    username = session["username"]
    print(username)
    parsed = json.loads(data)
    if parsed["type"] == "update_state":
        states[username] = parsed

        if username in player_room:
            room_id = player_room[username]
            for player_id in rooms[room_id]:
                if player_id != username:
                    socketio.emit(
                        "message",
                        json.dumps(states[username]),
                        room=sockets[player_id],
                    )

    elif parsed["type"] == "connect":
        player_id = username
        sockets[player_id] = request.sid

        room_id = parsed["room_id"]
        if room_id not in rooms:
            rooms[room_id] = []
        if len(rooms[room_id]) < 2:
            rooms[room_id].append(player_id)
            player_room[player_id] = room_id
            # socketio.join_room(request.sid, room_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Здесь должна быть ваша логика проверки учётных данных
        if authenticate(username, password):
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return "Login Failed"
    return render_template("login.html")


def authenticate(username, password):
    # Здесь должна быть ваша реализация проверки учётных данных
    return True


@app.route("/")
def index():
    if "username" in session:
        # Пользователь аутентифицирован, отобразить главную страницу
        return render_template("index.html", username=session["username"])
    # "Welcome, " + session["username"]
    else:
        # Пользователь не аутентифицирован, перенаправить на страницу логина
        return redirect(url_for("login"))


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=3000)
