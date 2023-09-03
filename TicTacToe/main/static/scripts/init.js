// GLOBAL VARIABLES
let grid;
let sequence;
let player;
let start;
let area = [];


// FUNCTIONS
function render_grid(update, data) {
    // Set new values to the global variables
    grid = data["grid"];

    if (update == false) {
        player = data["player"];
    }

    sequence = data["sequence"];  
    start = data["start"];

    document.getElementById("current_grid").textContent = "Grid: " + String(grid) + " |";
    document.getElementById("current_sequence").textContent = "Sequence: " + String(sequence) + " |";
    document.getElementById("current_player").textContent = "Player: " + String(start);

    // Organizing game area
    let tmp = document.getElementById("game_area");    

    // Deleting element's content
    if (update == true) {
        tmp.replaceChildren();
    }

    // Configurating game area
    tmp.style.gridTemplateColumns = `repeat(${grid}, auto)`;
    
    for (let i = 0; i < grid * grid; i++) {
        let new_div = document.createElement("div");

        new_div.setAttribute("class", "square");
        new_div.setAttribute("id", "square" + i);        

        tmp.appendChild(new_div);
    }

}

function update() {
    let check = []
    let check2 = [1, 2]

    for (let i = 3; i < 10; i++) {
        check[i - 3] = i;
    }

    tmp_grid = Number(document.getElementById("config_grid").value);
    tmp_seq = Number(document.getElementById("config_sequence").value);
    tmp_start = Number(document.getElementById("config_order").value);

    if (check.indexOf(tmp_grid) != -1 && check.indexOf(tmp_seq) != -1 && tmp_grid >= tmp_seq && check2.indexOf(tmp_start) != -1) {
        data = {
            "grid": tmp_grid,
            "sequence": tmp_seq,
            "start": tmp_start
        }

        socket.emit("update", {"room": x, "grid": tmp_grid, "sequence": tmp_seq, "start": tmp_start});
    }    
}


// SOCKETS
// Client Side
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
    render_grid(false, data);  
})

socket.on("handle_update", (data) => {
    render_grid(true, data);
})

socket.on("disconnect", () => {
    console.log("Disconnected from the server");
})

socket.on("close_lobby" , () => {
    window.location.href = "http://127.0.0.1:5000/"
})