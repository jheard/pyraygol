import pyraylib as rl
from pyraylib.colors import LIGHTGRAY, GREEN, RAYWHITE

from copy import deepcopy
import pygol.Glyph as Glyph
import pygol
from time import time
from math import floor, sqrt
from collections import deque
from functools import partial

BACK_COLOR = rl.Color(18, 75, 18, 255)
CELL_COLOR = rl.Color(124, 190, 255, 255)
GHOST_COLOR = rl.Color(124, 175, 227, 127)
LINE_COLOR = rl.Color(65, 107, 70, 255)

minmax = lambda a, b, c: min(max(a, b), c)

updates = []
board = pygol.Board()
MAX_LEN = 1000
boards = deque(maxlen=MAX_LEN)
boards.append(board)
currBoard = 0
pops = deque(maxlen=2000)
popsTriggered = False
popsTrigger = False
POP_GATE = 20
savedBoard = pygol.Board()
saved = False
numGlyphs = len(pygol.glyphs)
activeGlyph = numGlyphs
pastedGlyph = None
pastedString = ""

# Initialization
window = rl.Window((800, 450), "PyGol")
# Set our game to run at 60 frames-per-second
window.set_fps(60)
window.set_state(rl.WindowState.RESIZABLE)

DIM = 20

camera = rl.Camera2D(
    offset=(window.width / 2, window.height / 2),
    target=(window.width / 4, window.height / 4),
    rotation=0,
    zoom=1,
)

rBoxMode = False
rBoxmin = 1
rBoxmax = 100

rBox = rl.Vector2(1, 1)

paused = True
# Main game loop
statPrintDelay = 10
delay = statPrintDelay

dragging = False
rdragStart = rl.Vector2()
dragStartPoint = rl.Vector2()
dragEndPoint = rl.Vector2()
ldragdelay = 5

updates.append("frames,alive,setpops,time,fps")
while window.is_open():  # Detect window close button or ESC key
    # Update
    startTime = time()
    if window.is_file_dropped():
        files = window.get_dropped_files()
        try:
            for file in files:
                with open(file) as f:
                    fdata = f.read()
                g = {
                    "board": board,
                    "pygol": pygol,
                    
                }
                g['breakpoint'] = None
                g['callable'] = None
                g['compile'] = None
                g['eval'] = None
                g['exec'] = None
                g['exit'] = None
                g['help'] = None
                g['input'] = None
                g['memoryview'] = None
                g['open'] = None
                g['quit'] = None
                eval(compile(fdata,file,"exec"),g)
        except Exception as e:
            print(e)
    if not dragging and rl.is_mouse_button_down(rl.MouseButton.RIGHT_BUTTON):
        rdragStart = rl.get_mouse_position()
        dragging = True
    if rl.is_mouse_button_released(rl.MouseButton.RIGHT_BUTTON):
        dragging = False
    if dragging and rl.is_mouse_button_down(rl.MouseButton.RIGHT_BUTTON):
        delta = rl.get_mouse_position() - rdragStart
        delta = delta * -1.0 / camera.zoom
        camera.target += delta
        rdragStart = rl.get_mouse_position()
    wheel = rl.get_mouse_wheel_move()
    mouseWorld = camera.get_screen_to_world(rl.get_mouse_position())
    hovercell = (int(mouseWorld.x // DIM), int(mouseWorld.y // DIM))
    if abs(wheel):
        camera.offset = rl.get_mouse_position()
        camera.target = mouseWorld
        scaleF = 1.0 + (0.25 * abs(wheel))
        if wheel < 0:
            scaleF = 1.0 / scaleF
        camera.zoom = minmax(0.05, camera.zoom * scaleF, 10)
    if not dragging and rl.is_mouse_button_pressed(rl.MouseButton.LEFT_BUTTON):
        if rBoxMode:
            board.randomstamp(hovercell, rBox)
        else:
            hoverCellState = 1 if boards[currBoard].get(hovercell) else 0
            if activeGlyph == numGlyphs and not pastedGlyph:
                board[hovercell] = 0 if hoverCellState else 1
            elif pastedGlyph:
                board.stamp(*hovercell, pastedGlyph)
                pastedGlyph = None
            else:
                board.stamp(*hovercell, pygol.glyphs[activeGlyph])
    k = rl.get_key_pressed()
    match k:
        case rl.Keyboard.R:
            boards.clear()
            pops.clear()
            currBoard = 0
            updates = []
            delay = 0
            board = pygol.Board()
            boards.append(board)
            popsTriggered = False
            popsTrigger = False
            paused = True
        case rl.Keyboard.K:
            activeGlyph = (activeGlyph + 1) % (numGlyphs + 1)
        case rl.Keyboard.SEMICOLON:
            activeGlyph = (activeGlyph - 1) % (numGlyphs + 1)
        case rl.Keyboard.X:
            rBoxMode = not rBoxMode
        case rl.Keyboard.KP_4:
            step = 10 if rl.is_key_down(rl.Keyboard.LEFT_SHIFT) else 1
            rBox.x = minmax(rBoxmin, rBox.x - step, rBoxmax)
        case rl.Keyboard.KP_8:
            step = 10 if rl.is_key_down(rl.Keyboard.LEFT_SHIFT) else 1
            rBox.y = minmax(rBoxmin, rBox.y + step, rBoxmax)
        case rl.Keyboard.KP_6:
            step = 10 if rl.is_key_down(rl.Keyboard.LEFT_SHIFT) else 1
            rBox.x = minmax(rBoxmin, rBox.x + step, rBoxmax)
        case rl.Keyboard.KP_2:
            step = 10 if rl.is_key_down(rl.Keyboard.LEFT_SHIFT) else 1
            rBox.y = minmax(rBoxmin, rBox.y - step, rBoxmax)
        case rl.Keyboard.SPACE:
            paused = not paused
        case rl.Keyboard.F:
            if rBoxMode:
                board.setBox(hovercell,rBox,1)
        case rl.Keyboard.E:
            if rBoxMode:
                board.setBox(hovercell,rBox,0)
        case rl.Keyboard.V:
            if rl.is_key_down(rl.Keyboard.LEFT_CONTROL) or rl.is_key_down(rl.Keyboard.RIGHT_CONTROL):
                pastedGlyph = Glyph.from_str(window.clipboard_text)
                pastedString = window.clipboard_text
                print(pastedGlyph)
        case rl.Keyboard.C:
            if (rl.is_key_down(rl.Keyboard.LEFT_CONTROL) or rl.is_key_down(rl.Keyboard.RIGHT_CONTROL)):
                if (pastedGlyph and pastedGlyph.name == "Copied"):
                    window.clipboard_text = str(pastedGlyph)
                else:
                    code_string = boards[currBoard].to_glyph(hovercell,rBox)
                    code_string = Glyph.rle(code_string)
                    dims = rBox * 2 + 1
                    pastedGlyph = Glyph("Copied",*dims,code_string)
                    print(pastedGlyph)
    if paused:
        if k == rl.Keyboard.N:
            if currBoard == len(boards) - 1:
                board = board.advance()
                boards.append(board)
                pops.append(len(board))
                if (popsTrigger and len(set(pops)) <= pops.maxlen//POP_GATE and len(pops) == pops.maxlen):
                    paused = not paused
                    popsTriggered = True
                if not delay % statPrintDelay:
                    updates.append(
                        f"{delay},{len(boards[currBoard])},{(time() - startTime)*1000:0.2f},{window.get_fps()}"
                    )
                delay += 1
            currBoard = currBoard if currBoard == MAX_LEN - 1 else currBoard + 1
            board = boards[currBoard]
        if k == rl.Keyboard.B and currBoard > 0:
            currBoard -= 1
            board = boards[currBoard]
        if k == rl.Keyboard.S:
            savedBoard = deepcopy(boards[currBoard])
        if k == rl.Keyboard.L:
            board = deepcopy(savedBoard)
            boards[currBoard] = board
            
    elif not popsTriggered:
        if currBoard == len(boards) - 1:
            board = board.advance()
            boards.append(board)
        currBoard = currBoard if currBoard == MAX_LEN - 1 else currBoard + 1
        pops.append(len(board))
        if (popsTrigger and len(set(pops)) <= (pops.maxlen // POP_GATE) and len(pops) == pops.maxlen):
            paused = not paused
            popsTriggered = True
        if not delay % statPrintDelay:
            updates.append(
                f"{delay},{len(boards[currBoard])},{len(set(pops))},{(time() - startTime)*1000:0.2f},{window.get_fps()}"
            )
        delay += 1
    
    
    window.begin_drawing()
    window.clear_background(BACK_COLOR)
    camera.begin_mode()
    world_tl = camera.get_screen_to_world((0, 0))
    world_br = camera.get_screen_to_world(window.size)
    shadows = 0
    if shadows and len(boards) > shadows:
        for i in range(shadows):
            for cell in boards[currBoard-shadows+i].aliveCells():
                rl.draw_rectangle_v(rl.Vector2(*cell) * DIM, (DIM, DIM), CELL_COLOR.fade(i/shadows))
    else:
        for cell in board.aliveCells():
            rl.draw_rectangle_v(rl.Vector2(*cell) * DIM, (DIM, DIM), CELL_COLOR)
    #for i in range( int(world_tl.x-DIM)//DIM*DIM, int(world_br.x+DIM)//DIM*DIM, DIM):
    #    rl.draw_line((float(i),world_tl.y-DIM),(float(i),world_br.y+DIM),LINE_COLOR,sqrt(camera.zoom)/5)
    #for i in range(int(world_tl.y-DIM)//DIM*DIM,int(world_br.y+DIM)//DIM*DIM,DIM):
    #    rl.draw_line((world_tl.x-DIM,float(i)),(world_br.x+DIM,float(i)),LINE_COLOR,sqrt(camera.zoom)/5)
    if rBoxMode:
        rBoxtl = (rl.Vector2(*hovercell) + 1 + rBox) * DIM
        rBoxbr = (rl.Vector2(*hovercell) - rBox) * DIM
        thickness = camera.zoom
        rl.draw_rectangle_v(rBoxbr, (rBox * 2 + 1) * DIM, GHOST_COLOR)
    elif not pastedGlyph and activeGlyph == numGlyphs:
        tl = rl.Vector2(*hovercell) * DIM
        rl.draw_rectangle_v(tl, (DIM,DIM), GHOST_COLOR)
    elif pastedGlyph:
        for cell, state in pastedGlyph.parseglyph(*hovercell):
            rl.draw_rectangle_v(rl.Vector2(*cell) * DIM, (DIM, DIM), GHOST_COLOR)
    else:
        for cell, state in pygol.glyphs[activeGlyph].parseglyph(*hovercell):
            rl.draw_rectangle_v(rl.Vector2(*cell) * DIM, (DIM, DIM), GHOST_COLOR)
    camera.end_mode()
    text_spacing = 30
    y = 20
    window.draw_fps((20, y))
    y += text_spacing
    if paused:
        rl.draw_rectangle(window.width - 60, 20, 15, 40, rl.RED)
        rl.draw_rectangle(window.width - 40, 20, 15, 40, rl.RED)
    s = f"""\
Alive: {len(list(filter(None,board.values())))}\n\
State: {currBoard+1:3}/{len(boards)}\n\
Updates: {delay}\n\
Set Pops: {len(set(pops))}\n\
HoverCell: {hovercell}\n\
"""
    if rBoxMode:
        s += f"Box: ({int(rBox.x)*2+1}, {int(rBox.y)*2+1})\n"
    if activeGlyph != numGlyphs:
        s += f"Glyph: {pygol.glyphs[activeGlyph].name}\n"
    rl.draw_text(s, 20, y, 20, (48, 255, 48, 255))
    window.end_drawing()


# Close window and OpenGL context
window.close()

