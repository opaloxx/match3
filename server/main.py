from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import json

from handlers import connect, update_state

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")


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
    parsed = json.loads(data)
    if parsed["type"] == "update_state":
        for message, room in update_state(username, parsed):
            socketio.emit(
                "message", 
                json.dumps(message), 
                room=room
            )

    elif parsed["type"] == "connect":
        for message, room in connect(username, parsed["room_id"], request.sid):
            socketio.emit(
                "message", 
                json.dumps(message), 
                room=room
            )


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
        username = session["username"]
        return render_template("index.html", username=username)
    # "Welcome, " + session["username"]
    else:
        # Пользователь не аутентифицирован, перенаправить на страницу логина
        return redirect(url_for("login"))


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=3000)
