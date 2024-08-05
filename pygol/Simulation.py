from collections import deque
from time import time

from .Board import Board

class Simulation():
    """Simulation harness for the Game of Life"""
    update_header = "frames,alive,setpops,time,fps"

    def __init__(self, max_length: int = 1000) -> None:
        self.update_lines: list[dict] = []
        self.boards: deque = deque(maxlen=max_length)
        self.boards.append(Board())
        self.current: int = 0
        self.pops: deque = deque(maxlen=max_length*2)
        self.popsTriggered: bool = False
        self.popsTrigger: bool = False
        self.POP_GATE: int = 20
        self.updateSaveDelay: int = 10
        self.updates: int = 0
        self.paused: bool = True
    
    @property
    def board(self) -> Board:
        """The current board of the simulation"""
        return self.boards[self.current]

    @board.setter
    def board(self, value: Board) -> None:
        self.boards[self.current] = value
    
    @board.getter
    def board(self) -> Board:
        return self.boards[self.current]

    def reset(self) -> None:
        self.boards.clear()
        self.pops.clear()
        self.current = 0
        self.update_lines = []
        self.updates = 0
        self.boards.append(Board())
        self.popsTriggered = False
        self.popsTrigger = False
        self.paused = True
    
    def advance(self) -> None:
        if self.popsTriggered:
            return
        if self.current == len(self.boards) - 1:
            startTime = time()
            self.boards.append(self.board.advance())
            self.pops.append(len(self.board))
            if (self.popsTrigger and len(set(self.pops)) <= self.pops.maxlen//self.POP_GATE and len(self.pops) == self.pops.maxlen):
                self.paused = not self.paused
                self.popsTriggered = True
            if not self.updates % self.updateSaveDelay:
                self.update_lines.append({'count': self.updates, 'alive': len(self.board),'duration': (time() - startTime)*1000})
            self.updates += 1
        if self.current != self.boards.maxlen - 1:
            self.current + 1
    
    def step_back(self) -> None:
        if self.current > 0:
            self.current -= 1
    
    def toggle_pause(self) -> None:
        self.paused = not self.paused

    