# TicTacToe
## Video demo: https://youtu.be/4Bvcrr8yUFw

# App general description

## Home

It is separated in 2 parts, Lobby and Configurations.

Lobby - allows the user to join avaliable lobbies.

Configurations - allows the user to create their own lobby. The current options are:

    Grid - can be a number between 3 - 9.
    Sequence - can be a number between 3 - 9, but can't be greater than Grid.
    Password - can be blank or a number between 1 - 5 character.
    Id - must be a number with 3 character.

## Lobby

Contains Player Information and Lobby Information.

Player Information - shows players's status. The player 1 can only start the game if the player 2 press the ready button. Player 2 can request to restart the game.

Lobby Information - allows the player 1 to update the current configurations. Can't update when the game is ongoing nor when player 2 is ready.

### About the project in general

The current project was created using Flask framework mixed with SocketIO to make the game multiplayer (as the HTML is unique for each user, so the socket is helpful to connect the client to the server and the server can render to multiple clients). It also uses SQLite3 to help with data transfer and conditions.

Once an user creates a lobby, the lobby's information is sent to the database and the server dinamically renders it to the home area.

Inside the lobby, the socket communication is estabilished and, with the help of JavaScript, the page can listen to user's input.

### About the TicTacToe algorithm

I did the algorithm from my mind, so maybe it isn't the best one. But the way it works is based on every square's id. Once an user marks on a square, JavaScript get the player's symbol and place it inside an array with the index being the square's id and the array is sent to the server.

The server will loop through the array in many different ways, such as the win condition in TicTacToe, left to right, top to bottom, diagonally. The idea is that the game area is separated by row and column, if I want to move to another column, simply add 1. If I want to move to another row, add the value of the grid...

The array can hold three values, "x", "o" and "-". Once the server encounters a symbol, it will add the square's id into another array x[] or o[] and will clear the opposite symbol. Once the server encounters a "-" it will clear all arrays. If the length of x or o is == than the sequence condition, then there is a winner!



