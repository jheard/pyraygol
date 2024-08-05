import random
import re

class Board(dict):
    neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self, rule="B3/S23"):
        super().__init__()
        self.rule = rule
        born, survive = self.rule.split("/")
        self.born = set(map(int, re.findall(r"\d", born)))
        self.survive = set(map(int, re.findall(r"\d", survive)))

    def getNeighbors(self, cell):
        for n in self.neighbors:
            yield cell[0] + n[0], cell[1] + n[1]

    def isNeighborAlive(self, cell):
        for n in self.getNeighbors(cell):
            yield 1 if self.get(n) else 0

    def aliveCells(self):
        for c, i in self.items():
            if i:
                yield c

    def bounds(self, topleft, bottomright, edge, cell):
        if (topleft[0] - edge) < cell[0] < (bottomright[0] + edge):
            if (topleft[1] - edge) < cell[1] < (bottomright[1] + edge):
                return True
        return False
    
    def _iter_box(self,cell,rBox):
        endl = False
        for y in range(int(cell[1] - rBox[1]), int(cell[1] + rBox[1] + 1)):
            for x in range(int(cell[0]- rBox[0]), int(cell[0] + rBox[0] + 1)):
                yield (x,y), endl
                endl = False
            endl = True
    
    def boxBounds(self,cell,rBox):
        tl = min(self._iter_box(cell,rBox))
        br = max(self._iter_box(cell,rBox))
        return tl, br

    def stamp(self, startx, starty, glyph):
        for cell, state in glyph.parseglyph(startx, starty):
            self[cell] = state

    def randomstamp(self, c, rBox):
        for cell,_ in self._iter_box(c,rBox):
                if random.choice([0, 1]):
                    self[cell] = 1    
        
    def setBox(self, c, rBox, state):
        for cell,_ in self._iter_box(c,rBox):
            self[cell] = state
    
    def to_glyph(self,c,r):
        codestr = ""
        for cell,endl in self._iter_box(c,r):
            state = 'o' if self.get(cell,0) else 'b'
            if endl:
                codestr += "$"
            codestr += state
        return codestr
    
    def advance(self):
        newBoard = Board(rule=self.rule)
        for cell in self.keys():
            for nbor in self.getNeighbors(cell):
                nCount = sum(n for n in self.isNeighborAlive(nbor))
                if nCount in self.born or (nCount in self.survive and self.get(nbor,0) == 1):
                    newBoard[nbor] = 1
        return newBoard