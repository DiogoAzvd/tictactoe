# TicTacToe!

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
