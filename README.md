# learnpython
 
This folder contains small Python game projects.
 
## Snake Game (Python + Pygame)
 
[snake_game.py](file:///Users/chouisbo/Desktop/learnpython/snake_game.py) is a Snake game implemented with `pygame`.
 
### Features
 
- Snake movement with wrap-around edges (borderless playfield)
- Background grid
- A single horizontal obstacle line across the middle
- Food spawning and score counter
- Game Over screen
 
### Requirements
 
- Python 3 (recommended: 3.9+)
- `pygame`
 
Install pygame:
 
```bash
python3 -m pip install pygame
```
 
### Run
 
```bash
python3 snake_game.py
```
 
### Controls
 
- Arrow keys: move
- Close the window: quit
 
### Gameplay Rules
 
- Eat the red food to gain 1 score.
- The game ends if the snake hits itself or the obstacle line.
- If the snake crosses a screen edge, it appears on the opposite side.
 
### Configuration
 
You can edit these constants near the top of [snake_game.py](file:///Users/chouisbo/Desktop/learnpython/snake_game.py):
 
- `WIDTH`, `HEIGHT`: window size
- `CELL_SIZE`: grid size and snake movement step
- `clock.tick(10)`: game speed (FPS)
 
### Troubleshooting
 
- `ModuleNotFoundError: No module named 'pygame'`: run `python3 -m pip install pygame`
- If the window opens then closes immediately, run from a terminal to see the error output:
 
```bash
python3 snake_game.py
```
