from typing import Iterator
import random
import re

type Cell = tuple[int,int]
type State = int

from . import Glyph

class Board(dict):
    """Representation of the Game of Life"""
    neighbors: list[Cell] = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self, rule: str = "B3/S23") -> None:
        super().__init__()
        self.rule = rule
        born, survive = self.rule.split("/")
        self.born = set(map(int, re.findall(r"\d", born)))
        self.survive = set(map(int, re.findall(r"\d", survive)))

    def getNeighbors(self, cell: Cell) -> Iterator[Cell]:
        """Generate a list of neighbors for a cell"""
        for n in self.neighbors:
            yield cell[0] + n[0], cell[1] + n[1]

    def areNeighborsAlive(self, cell: Cell) -> Iterator[State]:
        """Generate a list of states of neighbors"""
        for n in self.getNeighbors(cell):
            yield 1 if self.get(n) else 0

    def aliveCells(self) -> Iterator[Cell]:
        """Generate a list of alive cells"""
        for c, i in self.items():
            if i:
                yield c

    def bounds(self, topleft: Cell, bottomright: Cell, edge: int, cell: Cell) -> bool:
        if (topleft[0] - edge) < cell[0] < (bottomright[0] + edge):
            if (topleft[1] - edge) < cell[1] < (bottomright[1] + edge):
                return True
        return False
    
    def _iter_box(self, cell: Cell, rBox: list[int]) -> Iterator[tuple[bool, Cell]]:
        """Generate a list of cells within the radius of rBox"""
        endl = False
        for y in range(int(cell[1] - rBox[1]), int(cell[1] + rBox[1])+1):
            for x in range(int(cell[0] - rBox[0]), int(cell[0] + rBox[0])+1):
                yield endl, (x,y)
                endl = False
            endl = True

    def stamp(self, startx: int, starty: int, glyph: Glyph) -> None:
        """Stamp glyph onto the board"""
        for cell, state in glyph.parseglyph(startx, starty):
            self[cell] = state

    def randomstamp(self, cell: Cell, rBox: list[int]) -> None:
        """Stamp cells within radius of rBox randomly"""
        for _,c in self._iter_box(cell,rBox):
            if random.choice([0, 1]):
                self[c] = 1    
        
    def setBox(self, cell:Cell, rBox: list[int], state: State) -> None:
        """Set the state of cells within radius of rBox"""
        for _,c in self._iter_box(cell,rBox):
            self[c] = state
    
    def to_glyph(self, cell: Cell, rBox: list[int]) -> str:
        """Generate glyphstring for cells within radius of rBox"""
        codestr = ""
        for endl, c in self._iter_box(cell,rBox):
            if endl:
                codestr += "$"
            state = self.get(c,0)
            codestr += 'o' if state else 'b'
        return codestr
    
    def advance(self) -> 'Board':
        """Generate a new board according to the rules"""
        newBoard = Board(rule=self.rule)
        for cell in self.keys():
            for nbor in self.getNeighbors(cell):
                nCount = sum(n for n in self.areNeighborsAlive(nbor))
                if nCount in self.born:
                    newBoard[nbor] = 1
                elif nCount in self.survive and self.get(nbor,0) == 1:
                    newBoard[nbor] = 1
        return newBoard