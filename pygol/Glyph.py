from copy import copy
from typing import Iterator
import enum
import re

from .Board import Cell, State

#x = 15, y = 6, rule = B3/S23
#bo11b2o$obo4bo6bo$7bo4bo$2bo2bo3bo2bo$2b2o6bo$3bo!
#Glyph from LifeWiki clipboard https://conwaylife.com/wiki/LifeViewer

class GlyphFlip(enum.Flag):
    """Enum for tracking state of a glyph"""
    NORMAL = enum.auto()
    HORIZONTAL = enum.auto()
    VERTICAL = enum.auto()
    BOTH = enum.auto()
    TRANSPOSE = enum.auto()

class Glyph():
    """A pattern from the Game of Life"""

    code_pattern = r"(\d*?[bBoO])(\d?\$)?"
    clip_pattern = r"(?:#N (?P<name>.*?).rle)?.*x = (?P<x>\d*), y = (?P<y>\d*), rule = (?P<rule>[Bb]\d*/[Ss]\d*)(?P<code>.*)"

    def __init__(self, name: str, x: int, y:int, code:str, rule:str="B3/S23", flip:GlyphFlip=GlyphFlip.NORMAL) -> None:
        self.name: str = name
        self.x: int = int(x)
        self.y: int = int(y)
        self.rule: str = rule
        self.code: str = code
        self.flip: GlyphFlip = flip
        self.array: list[list[int]] = []

    @classmethod
    def rle(cls,s:str) -> str:
        """Run-length encode a glyph string"""
        if not s:
            return ""

        s = re.sub(r"\$(b+?)[\$$]", '$$', s.lower())
        encoded = []
        count = 1
        previous = s[0]
        digraph = lambda n,c : f"{n if n > 1 else ''}{c}"

        for c in s[1:]:
            if c == previous:
                count += 1
            else:
                encoded.append(digraph(count,previous))
                previous = c
                count = 1
        encoded.append(digraph(count,c) + "!")
        s = ''.join(encoded)
        blankendings = re.findall(r"\d*b[\$!]",s)
        for b in set(blankendings):
            s = s.replace(b,b[-1])
        return s

    @classmethod
    def from_str(cls, s: str) -> 'Glyph | None':
        matches = re.match(cls.clip_pattern, s,re.MULTILINE|re.DOTALL)
        if not matches:
            return None
        name, x, y, rule, code = matches.groups()
        code = ''.join(code.split())
        if not name:
            name = "A Glyph"
        return Glyph(name,int(x),int(y),code,rule)

    def __str__(self) -> str:
        return f"#N {self.name}.rle\nx = {self.x}, y = {self.y}, rule = {self.rule}\n{self.code}"

    def __repr__(self) -> str:
        return f"Glyph({self.name!r},{self.x!r},{self.y!r},{self.code!r},{self.rule!r})"

    def parseglyph(self, bx: int, by:int) -> Iterator[tuple[Cell,State]]:
        """Parse the code string and generate a list of alive cells"""
        if not self.array:
            i = 0
            j = 0
            self.array = []
            line = []
            for section, endl in re.findall(self.code_pattern, self.code):
                count = int(section[:-1]) if section[:-1] else 1
                for _ in range(count):
                    if section[-1] == "o":
                        line.append(1)
                    else:
                        line.append(0)
                        i += 1
                if endl:
                    while len(line) < self.x:
                        line.append(0)
                        i += 1
                    self.array.append(copy(line))
                    if endl[:-1]:
                        for _ in range(int(endl[:-1])-1):
                            self.array.append([0]*self.x)
                            j += 1
                    line.clear()
                    i = 0
                    j += 1
            while len(line) < self.x:
                line.append(0)
            self.array.append(copy(line))
        if self.flip & GlyphFlip.VERTICAL:
            self.array.reverse()
        if self.flip & GlyphFlip.HORIZONTAL:
            for l in self.array:
                l.reverse()
        if self.flip & GlyphFlip.TRANSPOSE:
            self.array = list(zip(*self.array))
        for y, l in enumerate(self.array):
            for x, c in enumerate(l):
                if c:
                    yield (x+bx,y+by), 1