# Tetris Game - Pyxel Implementation

A clean, modular implementation of the classic Tetris game using the Pyxel game engine.

## Architecture Overview

The project is structured with clear separation of concerns:

```
src/
├── main.py       # Entry point and application loop
├── game.py       # Game logic and state management
├── board.py      # Board/grid management and collision detection
├── tetromino.py  # Tetromino shapes, rotations, and piece logic
└── renderer.py   # All rendering/drawing logic
```

### Component Responsibilities

#### `tetromino.py` - Piece Definitions
- Defines all 7 Tetromino shapes (I, O, T, S, Z, J, L)
- Manages piece rotation states
- Tracks piece position and color
- Provides block coordinate calculations

#### `board.py` - Game Board
- Manages the game grid (default 10x20)
- Handles collision detection
- Locks pieces into place
- Clears completed lines
- Checks game over conditions

#### `game.py` - Game Controller
- Orchestrates overall game flow
- Processes user input
- Manages game state (score, level, lines cleared)
- Handles piece spawning and movement
- Implements game mechanics (soft drop, hard drop, rotation)
- Controls game speed and difficulty progression

#### `renderer.py` - Display Layer
- Draws the game board and pieces
- Renders UI elements (score, next piece, controls)
- Shows ghost piece (landing preview)
- Displays game states (pause, game over)
- Handles all Pyxel drawing operations

#### `main.py` - Application Entry Point
- Initializes Pyxel
- Creates game and renderer instances
- Manages the main game loop
- Handles global controls (quit, restart)

## How to Run

1. Install dependencies:
   ```bash
   pip install pyxel
   ```

2. Run the game:
   ```bash
   python src/main.py
   ```

## Controls

- **Left/Right Arrow**: Move piece horizontally
- **Up Arrow / X**: Rotate piece clockwise
- **Z**: Rotate piece counterclockwise
- **Down Arrow**: Soft drop (faster falling)
- **Space**: Hard drop (instant placement)
- **P**: Pause game
- **R**: Restart game
- **Q / ESC**: Quit game

## Features

- **Classic Tetris Gameplay**: All 7 standard tetrominoes with proper colors
- **Ghost Piece**: Shows where the piece will land
- **Next Piece Preview**: See what's coming next
- **Scoring System**: Points for line clears and drops
- **Level Progression**: Game speeds up every 10 lines
- **Wall Kicks**: Smart rotation with position adjustments
- **Auto-Repeat**: Hold direction keys for continuous movement
- **Soft & Hard Drop**: Multiple ways to place pieces

## Design Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Readability**: Clear naming, comprehensive docstrings, logical organization
3. **Modularity**: Easy to modify or extend individual components
4. **Type Hints**: Function signatures include type annotations for clarity
5. **Constants**: Magic numbers avoided; configurable constants defined

## Extending the Game

The modular architecture makes it easy to extend:

- **Add new piece types**: Modify `tetromino.py` SHAPES dictionary
- **Change board size**: Pass different dimensions to `TetrisGame()`
- **Adjust game mechanics**: Modify constants in `game.py`
- **Customize visuals**: Edit drawing functions in `renderer.py`
- **Add sound effects**: Extend `game.py` with Pyxel sound calls
