import pyraylib as rl
from pyraylib.colors import LIGHTGRAY, GREEN, RAYWHITE

from copy import deepcopy
from pygol import Glyph
import pygol
from time import time

BACK_COLOR = rl.Color(18, 75, 18, 255)
CELL_COLOR = rl.Color(124, 190, 255, 255)
GHOST_COLOR = rl.Color(124, 175, 227, 127)
LINE_COLOR = rl.Color(65, 107, 70, 255)

clamp = lambda a, b, c: min(max(a, b), c)

simulation: pygol.Simulation = pygol.Simulation()
savedBoard: pygol.Board = pygol.Board()
saved = False
activeGlyph = pygol.num_glyphs
pastedGlyph = None
pastedString = ""


window = rl.Window((800, 450), "PyGol")
window.set_fps(60)
window.set_state(rl.WindowState.RESIZABLE)

CELL_DIM = 20

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
dragging = False
rdragStart = rl.Vector2()
dragStartPoint = rl.Vector2()
dragEndPoint = rl.Vector2()
ldragdelay = 5

# Main game loop
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
                    "board": simulation.board,
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
    hovercell = (int(mouseWorld.x // CELL_DIM), int(mouseWorld.y // CELL_DIM))
    if abs(wheel):
        camera.offset = rl.get_mouse_position()
        camera.target = mouseWorld
        scaleF = 1.0 + (0.25 * abs(wheel))
        if wheel < 0:
            scaleF = 1.0 / scaleF
        camera.zoom = clamp(0.05, camera.zoom * scaleF, 10)
    if not dragging and rl.is_mouse_button_pressed(rl.MouseButton.LEFT_BUTTON):
        if rBoxMode:
            simulation.board.randomstamp(hovercell, rBox)
        else:
            hoverCellState = 1 if simulation.board.get(hovercell) else 0
            if activeGlyph == pygol.num_glyphs and not pastedGlyph:
                simulation.board[hovercell] = 0 if hoverCellState else 1
            elif pastedGlyph:
                simulation.board.stamp(*hovercell, pastedGlyph)
                pastedGlyph = None
            else:
                simulation.board.stamp(*hovercell, pygol.glyphs[activeGlyph])
    k = rl.get_key_pressed()
    match k:
        case rl.Keyboard.R:
            simulation.reset()
            paused = True
        case rl.Keyboard.K:
            activeGlyph = (activeGlyph + 1) % (pygol.num_glyphs + 1)
        case rl.Keyboard.SEMICOLON:
            activeGlyph = (activeGlyph - 1) % (pygol.num_glyphs + 1)
        case rl.Keyboard.X:
            rBoxMode = not rBoxMode
        case rl.Keyboard.KP_4:
            step = 10 if rl.is_key_down(rl.Keyboard.LEFT_SHIFT) else 1
            rBox[0] = clamp(rBoxmin, rBox[0] - step, rBoxmax)
        case rl.Keyboard.KP_8:
            step = 10 if rl.is_key_down(rl.Keyboard.LEFT_SHIFT) else 1
            rBox[1] = clamp(rBoxmin, rBox[1] + step, rBoxmax)
        case rl.Keyboard.KP_6:
            step = 10 if rl.is_key_down(rl.Keyboard.LEFT_SHIFT) else 1
            rBox[0] = clamp(rBoxmin, rBox[0] + step, rBoxmax)
        case rl.Keyboard.KP_2:
            step = 10 if rl.is_key_down(rl.Keyboard.LEFT_SHIFT) else 1
            rBox[1] = clamp(rBoxmin, rBox[1] - step, rBoxmax)
        case rl.Keyboard.SPACE:
            simulation.toggle_pause()
            paused = not paused
        case rl.Keyboard.F:
            if rBoxMode:
                simulation.board.setBox(hovercell,rBox,1)
        case rl.Keyboard.E:
            if rBoxMode:
                simulation.board.setBox(hovercell,rBox,0)
        case rl.Keyboard.V:
            if rl.is_key_down(rl.Keyboard.LEFT_CONTROL) or rl.is_key_down(rl.Keyboard.RIGHT_CONTROL):
                pastedGlyph = Glyph.from_str(window.clipboard_text)
                pastedString = window.clipboard_text
                print(pastedGlyph)
        case rl.Keyboard.C:
            if (rl.is_key_down(rl.Keyboard.LEFT_CONTROL) or rl.is_key_down(rl.Keyboard.RIGHT_CONTROL)):
                if (pastedGlyph):
                    window.clipboard_text = str(pastedGlyph)
                else:
                    code_string = simulation.board.to_glyph(hovercell,rBox)
                    code_string = Glyph.rle(code_string)                   
                    dims = rBox * 2 + 1
                    pastedGlyph = Glyph("Copied",*dims,code_string)
        case rl.Keyboard.S:
            if ((rl.is_key_down(rl.Keyboard.LEFT_CONTROL) or rl.is_key_down(rl.Keyboard.RIGHT_CONTROL)) and pastedGlyph):
                pygol.glyphs.append(pastedGlyph)
                pygol.num_glyphs += 1
        case rl.Keyboard.COMMA:
            pygol.glyphs[activeGlyph].flip ^= pygol.GlyphFlip.HORIZONTAL
        case rl.Keyboard.PERIOD:
            pygol.glyphs[activeGlyph].flip ^= pygol.GlyphFlip.VERTICAL
        case rl.Keyboard.SLASH:
            pygol.glyphs[activeGlyph].flip ^= pygol.GlyphFlip.TRANSPOSE
    if paused:
        if k == rl.Keyboard.N:
            simulation.advance()
        if k == rl.Keyboard.B:
           simulation.step_back()
        if k == rl.Keyboard.S:
            savedBoard = deepcopy(simulation.board)
        if k == rl.Keyboard.L:
            simulation.board = deepcopy(savedBoard)
    else:
        simulation.advance()
    
    
    window.begin_drawing()
    window.clear_background(BACK_COLOR)
    camera.begin_mode()
    world_tl = camera.get_screen_to_world((0, 0))
    world_br = camera.get_screen_to_world(window.size)
    shadows = 0
    if shadows and len(simulation.boards) > shadows:
        for i in range(shadows):
            for cell in simulation.boards[simulation.current-shadows+i].aliveCells():
                rl.draw_rectangle_v(rl.Vector2(*cell) * CELL_DIM, (CELL_DIM, CELL_DIM), CELL_COLOR.fade(i/shadows))
    else:
        for cell in simulation.board.aliveCells():
            rl.draw_rectangle_v(rl.Vector2(*cell) * CELL_DIM, (CELL_DIM, CELL_DIM), CELL_COLOR)
    #for i in range( int(world_tl.x-DIM)//DIM*DIM, int(world_br.x+DIM)//DIM*DIM, DIM):
    #    rl.draw_line((float(i),world_tl.y-DIM),(float(i),world_br.y+DIM),LINE_COLOR,sqrt(camera.zoom)/5)
    #for i in range(int(world_tl.y-DIM)//DIM*DIM,int(world_br.y+DIM)//DIM*DIM,DIM):
    #    rl.draw_line((world_tl.x-DIM,float(i)),(world_br.x+DIM,float(i)),LINE_COLOR,sqrt(camera.zoom)/5)
    if rBoxMode:
        rBoxtl = (rl.Vector2(*hovercell) + 1 + rBox) * CELL_DIM
        rBoxbr = (rl.Vector2(*hovercell) - rBox) * CELL_DIM
        rl.draw_rectangle_v(rBoxbr, (rBox * 2 + 1) * CELL_DIM, GHOST_COLOR)
    elif not pastedGlyph and activeGlyph == pygol.num_glyphs:
        tl = rl.Vector2(*hovercell) * CELL_DIM
        rl.draw_rectangle_v(tl, (CELL_DIM,CELL_DIM), GHOST_COLOR)
    elif pastedGlyph:
        for cell, state in pastedGlyph.parseglyph(*hovercell):
            rl.draw_rectangle_v(rl.Vector2(*cell) * CELL_DIM, (CELL_DIM, CELL_DIM), GHOST_COLOR)
    else:
        for cell, state in pygol.glyphs[activeGlyph].parseglyph(*hovercell):
            rl.draw_rectangle_v(rl.Vector2(*cell) * CELL_DIM, (CELL_DIM, CELL_DIM), GHOST_COLOR)
    camera.end_mode()
    text_spacing = 30
    y = 20
    window.draw_fps((20, y))
    y += text_spacing
    if paused:
        rl.draw_rectangle(window.width - 60, 20, 15, 40, rl.RED)
        rl.draw_rectangle(window.width - 40, 20, 15, 40, rl.RED)
    s = f"""\
Alive: {len(list(filter(None,simulation.board.values())))}\n\
State: {simulation.current+1:3}/{len(simulation.boards)}\n\
Updates: {simulation.updates}\n\
Set Pops: {len(set(simulation.pops))}\n\
HoverCell: {hovercell}\n\
"""
    if rBoxMode:
        s += f"Box: ({int(rBox.x)*2+1}, {int(rBox.y)*2+1})\n"
    if activeGlyph != pygol.num_glyphs:
        s += f"Glyph: {pygol.glyphs[activeGlyph].name}\n"
    elif pastedGlyph:
        s += f"Glyph: {pastedGlyph.name}\n"
    rl.draw_text(s, 20, y, 20, (48, 255, 48, 255))
    window.end_drawing()


# Close window and OpenGL context
window.close()

