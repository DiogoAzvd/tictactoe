from flask import Flask, render_template, g, request, redirect
from flask_socketio import SocketIO, join_room, emit
import json
import sqlite3
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, ping_interval = 5000, ping_timeout = 120000)

DATABASE = "C:\\Users\\user\\Desktop\\TicTacToe\\info.db"


# FUNCTIONS


def check(data, start, end):
    compare = []

    for i in range(start, end):
        compare.append(i)

    return data in compare


def db_to_dict(cursor):
    column_names = [col[0] for col in cursor.description]

    data = [dict(zip(column_names, row))
            for row in cursor]
    data = data[0]

    return data


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


# Fetch makes the data avaliable to the app
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def win_condition(game_array, grid, sequence, room):
    x = []
    o = []

    # For left to right

    for i in range(grid):
        x.clear()
        o.clear()

        for j in range(grid):
            if game_array[j + i * grid] == "x":
                x.append(j + i * grid)
                o.clear()

                if len(x) == sequence:
                    data = {
                        "game_array": x,
                        "symbol": "x"
                    }

                    emit("win", data, to=room)
                    return 0
                    

            elif game_array[j + i * grid] == "o":
                o.append(j + i * grid)
                x.clear()

                if len(o) == sequence:
                    data = {
                        "game_array": o,
                        "symbol": "o"
                    }

                    emit("win", data, to=room)
                    return 0

            else:
                x.clear()
                o.clear()

    # Top to bottom

    for i in range(grid):
        x.clear()
        o.clear()

        for j in range(grid):
            if game_array[i + j * grid] == "x":
                x.append(i + j * grid)
                o.clear()

                if len(x) == sequence:
                    data = {
                        "game_array": x,
                        "symbol": "x"
                    }

                    emit("win", data, to=room)
                    return 0

            elif game_array[i + j * grid] == "o":
                o.append(i + j * grid)
                x.clear()

                if len(o) == sequence:
                    data = {
                        "game_array": o,
                        "symbol": "o"
                    }

                    emit("win", data, to=room)
                    return 0

            else:
                x.clear()
                o.clear()

    # Diagonal \ middle to left

    for i in range(grid):
        x.clear()
        o.clear()

        for j in range(grid - i):
            if game_array[i * grid + j + j * grid] == "x":
                x.append(i * grid + j + j * grid)
                o.clear()

                if len(x) == sequence:
                    data = {
                        "game_array": x,
                        "symbol": "x"
                    }

                    emit("win", data, to=room)
                    return 0

            elif game_array[i * grid + j + j * grid] == "o":
                o.append(i * grid + j + j * grid)
                x.clear()

                if len(o) == sequence:
                    data = {
                        "game_array": o,
                        "symbol": "o"
                    }

                    emit("win", data, to=room)
                    return 0

            else:
                x.clear()
                o.clear()

    # Diagonal \ middle to right

    for i in range(grid):
        x.clear()
        o.clear()

        for j in range(grid - i):
            if game_array[i + j + j * grid] == "x":
                x.append(i + j + j * grid)
                o.clear()

                if len(x) == sequence:
                    data = {
                        "game_array": x,
                        "symbol": "x"
                    }

                    emit("win", data, to=room)
                    return 0

            elif game_array[i + j + j * grid] == "o":
                o.append(i + j + j * grid)
                x.clear()

                if len(o) == sequence:
                    data = {
                        "game_array": o,
                        "symbol": "o"
                    }

                    emit("win", data, to=room)
                    return 0

            else:
                x.clear()
                o.clear()

    # Diagonal / middle to left

    for i in range(grid):
        x.clear()
        o.clear()

        for j in range(grid - i):
            if game_array[grid - 1 + j * grid - j - i] == "x":
                x.append(grid - 1 + j * grid - j - i)
                o.clear()

                if len(x) == sequence:
                    data = {
                        "game_array": x,
                        "symbol": "x"
                    }

                    emit("win", data, to=room)
                    return 0

            elif game_array[grid - 1 + j * grid - j - i] == "o":
                o.append(grid - 1 + j * grid - j - i)
                x.clear()

                if len(o) == sequence:
                    data = {
                        "game_array": o,
                        "symbol": "o"
                    }

                    emit("win", data, to=room)
                    return 0

            else:
                x.clear()
                o.clear()


    # Diagonal / middle to right

    for i in range(grid):
        x.clear()
        o.clear()

        for j in range(grid - i):
            if game_array[grid - 1 + j * grid - j + i * grid] == "x":
                x.append(grid - 1 + j * grid - j + i * grid)
                o.clear()

                if len(x) == sequence:
                    data = {
                        "game_array": x,
                        "symbol": "x"
                    }

                    emit("win", data, to=room)
                    return 0

            elif game_array[grid - 1 + j * grid - j + i * grid] == "o":
                o.append(grid - 1 + j * grid - j + i * grid)
                x.clear()

                if len(o) == sequence:
                    data = {
                        "game_array": o,
                        "symbol": "o"
                    }

                    emit("win", data, to=room)
                    return 0

            else:
                x.clear()
                o.clear()

    return 1


def set_game_area(grid):
    game_area = {}

    for i in range(int(grid) * int(grid)):
        game_area[str(i)] = "-"

    game_area = str(game_area)
    game_area = game_area.replace("'", '"')
    return game_area


# ROUTES


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        tmp = query_db("SELECT * FROM info")
        tmp_list = []
        info = []

        for i in tmp:
            for j in range(3, 8):
                tmp_list.append(i[j])

                if j == 7:
                    # Append room name
                    tmp_list.append(i[0])

            info.append(tmp_list.copy())
            tmp_list.clear()

        # Get amount of lobbies
        info_len = len(info)

        return render_template("/home.html", info=info, info_len=info_len)
    
    elif request.method == "POST":
        grid = request.form.get("grid")
        sequence = request.form.get("sequence")
        id = request.form.get("id")
        password = request.form.get("password")

        if check(grid, 3, 10) or check(sequence, 3, 10):
            return redirect("/")

        if int(grid) < int(sequence):
            return redirect("/")

        if len(id) != 3:
            return redirect("/")          
        
        for i in range(len(id)):
            if not check(int(id[i]), 0, 10):
                return redirect("/")        
            
        if len(password) >= 1:
            for i in range(len(password)):
                if not check(int(password[i]), 0, 10):
                    return redirect("/")             
                
        url = str(uuid.uuid4())

        lobby_id = query_db("SELECT room FROM info")
        lobbies = []

        for i in lobby_id:
            lobbies.append((i[0]))

        # Checking if the lobby exist
        while url in lobbies:
            url = str(uuid.uuid4())

        game_area = set_game_area(grid)

        config = [url, None, None, 0, grid, sequence, id, password, 0, 1, game_area]

        db = get_db()
        db.executemany("INSERT INTO info VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (config,))
        db.commit()
        db.close()
               
        return redirect(f"/lobby/{url}")
        # After the redirect, get information via query


@app.route("/lobby/<name>", methods=["GET", "POST"])
def lobby(name):    
    # Name is used to get data from the database
    if request.method == "GET":
        tmp = query_db("SELECT * FROM info WHERE room = ?", (name,))

        try:
            current_players = tmp[0][3]
        
        except IndexError:
            return redirect("/")
        
        password = tmp[0][7]

        # If the room doesn't require password
        if not password:
            if current_players == 0:
                return render_template("/lobby.html", room=name, player="player1")  

            elif current_players == 1:
                return render_template("/lobby.html", room=name, player="player2")
            
            else:
                return render_template("/full.html")

        # If the room requires password     
        else:
            return render_template("/confirm.html", url=name)        
    
    if request.method == "POST":
        tmp = query_db("SELECT * FROM info WHERE room = ?", (name,))
        user_input = request.form.get("confirm_password")
        current_players = tmp[0][3]
        password = tmp[0][7]

        if user_input == password:         
            
            if current_players == 0:
                return render_template("/lobby.html", room=name, player="player1")

            elif current_players == 1:
                return render_template("/lobby.html", room=name, player="player2")
            
            else:
                return render_template("/full.html")

        else:
            return render_template("/confirm.html", url=name, error=1)


@app.route("/closed", methods=['GET', 'POST'])
def closed():
    return render_template("closing_lobby.html")


# SOCKETS


@socketio.on("connected")
def handle_setup(lobby):
    db = get_db()
    tmp = db.execute("SELECT * FROM info WHERE room = ?", (lobby["room"],))
    
    for i in tmp:
        current_players = i[3]

    if current_players == 0:
        db.execute("UPDATE info SET current_players = 1, player1 = ? WHERE room = ?", (lobby["id"], lobby["room"],))
        db.commit()
        join_room(lobby["room"], lobby["id"])

        tmp = db.execute("SELECT * FROM info WHERE room = ?", (lobby["room"],))
        data = db_to_dict(tmp)        
        db.close()
    
        emit("connect_setup", data, to=data["player1"])

    elif current_players == 1:
        db.execute("UPDATE info SET current_players = 2, player2 = ? WHERE room = ?", (lobby["id"], lobby["room"],))
        db.commit()
        join_room(lobby["room"], lobby["id"])

        tmp = db.execute("SELECT * FROM info WHERE room = ?", (lobby["room"],))
        data = db_to_dict(tmp)
        db.close()
    
        emit("connect_setup", data, to=data["player2"])
        emit("player2_connected", to=data["room"])
        
    else:
        return redirect("/")


@socketio.on("disconnect")
def handle_connection():
    user_id = request.sid

    db = get_db()

    tmp = db.execute("SELECT * FROM info WHERE player1 = ? OR player2 = ?", (user_id, user_id,))

    for i in tmp:
        room = i[0]

    try:
        emit("closing_lobby", to=room)
        db.execute("DELETE FROM info WHERE room = ?", (room,))
        db.commit()
        db.close()

    except UnboundLocalError:
        pass
    

@socketio.on("update_db")
def handle_update(info):    
    game_area = set_game_area(info["grid"])

    db = get_db()
    db.execute("UPDATE info SET grid = ?, sequence = ?, start = ?, game_area = ? WHERE room = ?", (info["grid"], info["sequence"], info["start"], game_area, info["room"]))
    db.commit()
    db.close() 

    emit("update_setup", info, to=info["room"])


@socketio.on("start")
def handle_start(data):
    db = get_db()
    tmp = db.execute("SELECT * FROM info WHERE room = ?", (data["room"],))

    for i in tmp:
        grid = i[4]
        sequence = i[5]

    db.execute("UPDATE info SET grid = ?, sequence = ? WHERE room = ?", (grid, sequence, data["room"],))
    db.commit()

    tmp = db.execute("SELECT * FROM info WHERE room = ?", (data["room"],))

    new_data = db_to_dict(tmp)

    emit("start", new_data, to=data["room"])
    db.close()


@socketio.on("update_listener")
def handle_update_listener(data, position, symbol):
    db = get_db()
    db.execute("UPDATE info SET turn = ?, game_area = ? WHERE room = ?", (data["turn"], data["game_area"], data["room"],))
    tmp = db.execute("SELECT * FROM info WHERE room = ?", (data["room"],))

    info = db_to_dict(tmp)

    tmp_check = json.loads(info["game_area"])
    game_array = []

    for i in range(len(tmp_check)):
        game_array.append(tmp_check[str(i)])

    if win_condition(game_array, data["grid"], data["sequence"], data["room"]) == 0:
        return

    mark = {
        "position": position,
        "symbol": symbol
    } 

    emit("update_listener", info, to=data["room"])
    emit("mark", mark, to=data["room"])
    db.close()
    

@socketio.on("ready")
def handle_ready(data):
    emit("ready", to=data["room"])


@socketio.on("confirm")
def handle_confirm(data):
    db = get_db()

    game_area = set_game_area(data["grid"])

    db.execute("UPDATE info SET turn = 1, game_area = ? WHERE room = ?", (game_area, data["room"],))
    db.commit()

    emit("confirm", data, to=data["room"])
    db.close()


@socketio.on("enable_ready")
def handle_enable_ready(data):
    emit("enable_ready", to=data["room"])
    

@socketio.on("restart")
def handle_ready(data):
    emit("restart", to=data["room"])


if __name__ == '__main__':
    socketio.run(app, debug=True)