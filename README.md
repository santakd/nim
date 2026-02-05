## 🎲 Welcome to Nim! 🎲

Think this is just a bunch of sticks? Think again. Nim is a deceptively simple game of strategy, foresight, and just a tiny bit of mischief.
The rules are easy: take turns removing sticks from a single row. The twist? Nobody wants to take the last one. Leave your opponent staring at that lonely final stick, and victory is yours.
Every move matters. One careless grab and—oops—you’ve handed your opponent the win. Play smart, think ahead, and try not to look too suspicious when you leave them with “just one.”
Whether you’re here to outwit the AI, challenge a friend, or watch two machines battle it out in silent calculation, Nim promises clever tactics, zero luck, and absolutely no draws.
Ready to make your move?
Choose wisely… 🧠✨

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

## Tests

If you add unit tests, include instructions to run them here (for example, using pytest):

```bash
pip install pytest
pytest
```

## License

MIT License.

## Contact

If you have questions or suggestions, open an issue or submit a pull request. Mention @santakd for visibility.
