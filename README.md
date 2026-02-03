# nim
## Objective

Design a two-player strategic game called Take 1, where the objective is to force your opponent to be left with exactly one stick. 
The player who is left with the final single stick loses the game. 
Every move should therefore be made with the goal of leaving your opponent with one remaining stick.

## Game Configuration

The game board consists of three rows of sticks:

Row 1: 3 sticks

Row 2: 5 sticks

Row 3: 7 sticks

The game begins with a total of 15 sticks.

## Game Rules

The game is played by two players taking alternating turns.

On a player’s turn:

They may remove one or more sticks.

All removed sticks must come from exactly one row.

Removing sticks from multiple rows in a single turn is not allowed.

Players continue alternating turns until the game reaches a terminal state.

The game ends when only one stick remains on the board.

The player who is left with that final stick loses the game.

## Uniqueness & Guarantees

The game is deterministic, finite, and has perfect information.

The game is guaranteed to never result in a draw — one player must always lose.

## Gameplay Modes

Human vs AI

Human vs Human

AI vs AI (autoplay / simulation mode)

## Difficulty Levels

Easy – Random or shallow-depth strategy

Medium – Depth-limited Minimax with Alpha–Beta pruning

Hard – Full optimal Minimax with Alpha–Beta pruning (perfect play)

Difficulty selection should affect only AI players and be configurable at game start.
