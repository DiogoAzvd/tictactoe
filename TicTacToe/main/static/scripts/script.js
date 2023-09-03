// SOCKETS


const socket = io({
    pingInterval: 5000,
    pingTimeout: 120000,
    reconnection: false,
    reconnectionAttempts: 0
})


// On connecting, send message to the server
socket.on("connect", () => {
    // Arg(name of the handler function, data to send)
    socket.emit("connected", {room: x, id: socket.id});
})


socket.on("connect_setup", (data) => {
    setup_grid(data, false);  
})


socket.on("update_setup", (data) => {
    setup_grid(data, true);
})


socket.on("start", (data) => {
    document.getElementById("player2").innerHTML = 'Player 2 - <span style="color: #0f0;">Connected</span>';

    let restart_button = document.getElementById("restart_button");
    let ready_button = document.getElementById("ready");
    let start_button = document.getElementById("start");

    if (restart_button != null) {
        turn_off_on("restart_button", "on");
    }

    if (start_button != null) {
        turn_off_on("start", "off")
    }

    if (ready_button != null) {
        turn_off_on("ready", "off");
    }

    start(data);
})


socket.on("update_listener", (data) => {
    let text = document.getElementById("turn").textContent;
    console.log(text);

    if (text === "Player 1") {
        document.getElementById("turn").textContent = "Player 2";
    }

    else {
        document.getElementById("turn").textContent = "Player 1";
    }

    start(data);
})


socket.on("player2_connected", () => {
    document.getElementById("player2").innerHTML = 'Player 2 - <span style="color: #0f0;">Connected</span>';
})


socket.on("closing_lobby", () => {
    window.location.href = "http://127.0.0.1:5000/closed";
})


socket.on("confirm", (data) => {
    for (let i = 0; i < data["grid"] * data["grid"]; i++) {
        let square_id = document.getElementById("square" + i);

        square_id.removeEventListener("click", square_setup);
        square_id.style.backgroundImage = "none";
    }

    turn_off_on("confirm_button", "off");
    turn_off_on("update_button", "on");

    let restart_status = document.getElementById("restart_status");

    if (restart_status != null) {
        document.getElementById("restart_status").innerHTML = "Restart Game - 0 / 1";
    }    
    
    socket.emit("enable_ready", data);
})


socket.on("enable_ready", () => {
    turn_off_on("ready", "on");
})


socket.on("ready", () => {
    document.getElementById("player2").innerHTML = 'Player 2 - <span style="color: #08f;">Ready</span>';

    let start_button = document.getElementById("start");
    let update_button = document.getElementById("update");

    if (start_button != null) {
        turn_off_on("start", "on");    
    }

    if (update_button != null) {
        turn_off_on("update_button", "off");
    }
})


socket.on("restart", () => {
    let confirm_button = document.getElementById("confirm_button");
    let restart_status = document.getElementById("restart_status");
    let restart_button = document.getElementById("restart_button");

    if (confirm_button != null) {
        turn_off_on("confirm_button", "on");
    }

    if (restart_status != null) {
        document.getElementById("restart_status").innerHTML = "Restart Game - 1 / 1";
    }

    if (restart_button != null) {
        turn_off_on("restart_button", "off");
    }
})


socket.on("mark", (mark) => {
    if (mark["symbol"] == "x") {
        document.getElementById("square" + mark["position"]).style.backgroundImage = "url(/static/css/x.png)";
    }

    else if (mark["symbol"] == "o") {
        document.getElementById("square" + mark["position"]).style.backgroundImage = "url(/static/css/circle.png)";
    }
})


socket.on("win", (data) =>{
    for (let i = 0; i < data["game_array"].length; i++) {
        if (data["symbol"] == "x") {
            document.getElementById("square" + data["game_array"][i]).style.backgroundImage = "url(/static/css/x_win.png)";
        }

        else if (data["symbol"] == "o") {
            document.getElementById("square" + data["game_array"][i]).style.backgroundImage = "url(/static/css/circle_win.png)";
        }
    }
})


// FUNCTIONS


function turn_off_on(button, action) {
    let tmp = document.getElementById(button);

    if (tmp != null) {
        if (action == "off") {
            tmp.disabled = true;
            tmp.style.backgroundColor = "rgba(17, 17, 17, .5)";
            tmp.style.color = "rgba(255, 255, 255, .5)";
        }

        else if (action == "on") {
            tmp.disabled = false;
            tmp.style.backgroundColor = "rgba(17, 17, 17, 1)";
            tmp.style.color = "rgba(255, 255, 255, 1)";
        }
    }
}


// Update can be false or true  
function setup_grid(data, update) {
    // Updating lobby info 
    document.getElementById("current_grid").textContent = "Grid: " + data["grid"] + " |";
    document.getElementById("current_sequence").textContent = "Sequence: " + data["sequence"] + " |";
    document.getElementById("current_player").textContent = "Player: " + (data["start"] + 1);

    if (data["start"] == 0) {
        document.getElementById("turn").textContent = "Player 1";
    }

    else {
        document.getElementById("turn").textContent = "Player 2";
    }
    

    let tmp = document.getElementById("game_area");

    // Deleting element's content
    if (update == true) {
        tmp.replaceChildren();
    }

    // Configurating game area
    tmp.style.gridTemplateColumns = `repeat(${data["grid"]}, auto)`;
    
    for (let i = 0; i < data["grid"] * data["grid"]; i++) {
        let new_div = document.createElement("div");

        new_div.setAttribute("class", "square");
        new_div.setAttribute("id", "square" + i);        

        tmp.appendChild(new_div);
    }

    set_buttons(data);
}


function change_data(room) {
    let grid = Number(document.getElementById("config_grid").value);
    let sequence = Number(document.getElementById("config_sequence").value);

    if (sequence > grid) {
        return;
    }

    let data = {
        "grid": grid,
        "sequence": sequence,
        "start": Number(document.getElementById("config_order").value) - 1,
        "room": room
    };    

    if (compare(data["grid"], 3, 10) && compare(data["sequence"], 3, 10) && compare(data["start"], 0, 2)) {
        socket.emit("update_db", data);     
    }
}


function compare(data, start, end) {
    let check = [];

    for (let i = start; i < end; i++) {
        check[i - start] = i;
    }

    if (check.indexOf(data) != -1) {
        return true;
    }
    return false;
}


function square_setup(evt) {
    let data = evt.currentTarget.info;  

    if (data["player1"] == socket.id && (data["start"] + data["turn"]) % 2 == 1) {
        let tmp = JSON.parse(data["game_area"]);
        let position = String(evt.target.id);
        position = position.replace("square", "");

        if (tmp[position] == "-") {
            tmp[position] = "x";
            tmp = JSON.stringify(tmp);
            
            data["game_area"] = tmp;
            data["turn"] = Number(data["turn"]) + 1;                    

            socket.emit("update_listener", data, position, "x");
        }
    }
    
    else if (data["player2"] == socket.id && (data["start"] + data["turn"]) % 2 == 0) {
        let tmp = JSON.parse(data["game_area"]);
        let position = String(evt.target.id);
        position = position.replace("square", "");

        if (tmp[position] == "-") {
            tmp[position] = "o";
            tmp = JSON.stringify(tmp);
            
            data["game_area"] = tmp;
            data["turn"] = Number(data["turn"]) + 1;                    

            socket.emit("update_listener", data, position, "o");
        }
    }        
}

function start(data) {
    for (let i = 0; i < data["grid"] * data["grid"]; i++) { 
        let square_id = document.getElementById("square" + i);
        square_id.addEventListener("click", square_setup, false);
        square_id.info = data;
    }                 
}

function set_buttons(data) {
    let start_button = document.getElementById("start");

    if (start_button != null) {
        turn_off_on("start", "off");

        start_button.addEventListener("click", () => {
            socket.emit("start", data);
        })
    }

    let update_button = document.getElementById("update_button");
    
    if (update_button != null) {
        update_button.addEventListener("click", () => {
            change_data(data["room"]);
        })
    }

    let confirm_button = document.getElementById("confirm_button");

    if (confirm_button != null) {
        turn_off_on("confirm_button", "off");

        confirm_button.addEventListener("click", () => {
            socket.emit("confirm", data);
        })
    }

    let ready_button = document.getElementById("ready");

    if (ready_button != null) {
        ready_button.addEventListener("click", () => {
            socket.emit("ready", data);
        })
    }

    let restart_button = document.getElementById("restart_button");
    if (restart_button != null) {
        turn_off_on("restart_button", "off");

        restart_button.addEventListener("click", () => {
            socket.emit("restart", data);
        })
    }
}