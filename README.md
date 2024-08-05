# Description
An implementation of the Game of Life in Python.

## GUI
- `Alive`: Number of alive cells
- `State`: Current / Length of simulation state buffer
- `Updates`: Total steps of simulation
- `Set pops`: The length of the set of the last 2000 populations, useful for cycle detection
- `Hovercell`: Coords of cell under mouse
- `R.Box`: The radius during box mode
- `Glyph`: Glyph name when active

## Keybindings  
- `SPACE`: Pause  
- `R`: Reset  
- `K/;`: Cycle through glyph library  
- `Ctrl+V`: Import string from clipboard to glyph buffer.
- `Ctrl+C`: Copy glyph buffer to clipboard as string.  
- `Click`: Toggle cell or stamp glyph. (Glyph buffer clears on stamp)
- `X`: Toggles Box mode  
Box Mode:  
  - `Num 2/8`: -/+ Box height (Shift for -/+ 10)  
  - `Num 4/6`: -/+ Bow width (Shift for -/+ 10)  
  - `F`: Fill box  
  - `E`: Empty box  
  - `Click`: Randomize box  
  - `Ctrl+C`: Copy box to glyph buffer

While Paused:  
- `S`: Save current board to buffer  
- `L`: Load board from buffer  
- `B`: Step backward  
- `N`: Step forward  
  
 

## Features

1. Can simulate the game of life
2. 2D Camera allows for scrolling and zooming.
3. 1000 steps of rewind, adjustable in code.
4. Able to import/export rle strings from LifeWiki and other places.
5. Drop a python script to execute it in the context of the simulation.
     - Context includes reference to current board and pygol module. 
7. Keeps statistics, though not much output for them.
8. Able to detect pattern stalls, but off by default (Needs *much* improvement)
9. Shadow drawing (Off by default, needs work)
