import re
import enum
from typing import Iterator

from .Board import Cell, State

#x = 15, y = 6, rule = B3/S23
#bo11b2o$obo4bo6bo$7bo4bo$2bo2bo3bo2bo$2b2o6bo$3bo!
#Glyph from LifeWiki clipboard https://conwaylife.com/wiki/LifeViewer

class GlyphFlip(enum.Enum):
    """Enum for tracking state of a glyph"""
    NORMAL = enum.auto()
    HORIZONTAL = enum.auto()
    VERTICAL = enum.auto()
    BOTH = enum.auto()
    TRANSPOSE = enum.auto()

class Glyph():
    """A pattern from the Game of Life"""

    code_pattern = r"(\d*?[bBoO])(\d?\$)?"
    clip_pattern = r"x = (\d*), y = (\d*), rule = ([Bb]\d*/[Ss]\d*)"

    def __init__(self, name: str, x: int, y:int, code:str, rule:str="B3/S23", flip:GlyphFlip=GlyphFlip.NORMAL) -> None:
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.rule: str = rule
        self.code: str = code
        self.flip: GlyphFlip = flip

    @classmethod
    def rle(cls,s:str) -> str:
        """Run-length encode a glyph string"""
        if not s:
            return ""

        s = re.sub(r"\$(b*)\$", '$$', s.lower())
        encoded = []
        count = 1
        previous = s[0]
        digraph = lambda n,c : f"{n if n > 1 else ''}{c}"

        for c in s[1:]:
            if c == previous:
                count += 1
            else:
                if len(encoded) and previous == 'b' and encoded[-1][-1] == 'o' and c == "$":
                    pass
                elif not encoded and previous == 'b' and c == '$':
                    pass
                else:
                    encoded.append(digraph(count,c))
                previous = c
                count = 1

        encoded.append(digraph(count,c) + "!")
        return ''.join(encoded)

    @classmethod
    def from_str(cls, s: str) -> 'Glyph | None':
        _, *code = s.splitlines()
        matches = re.match(cls.clip_pattern, s,re.MULTILINE)
        if not matches:
            return None
        x, y, rule = matches.groups()
        return Glyph("Pasted Glyph",int(x),int(y),''.join(code),rule)

    def __str__(self) -> str:
        return f"x = {int(self.x)}, y = {int(self.y)}, rule = {self.rule}\n{self.code}"

    def __repr__(self) -> str:
        return f"Glyph({self.name!r},{self.x!r},{self.y!r},{self.code!r},{self.rule!r})"

    def parseglyph(self, starti: int, startj:int) -> Iterator[tuple[Cell,State]]:
        """Parse the code string and generate a list of alive cells"""
        i = starti
        j = startj
        for section, endl in re.findall(self.code_pattern, self.code):
            count = int(section[:-1]) if section[:-1] else 1
            for _ in range(count):
                if section[-1] == "o":
                    yield (i, j), 1
                i += 1
            if endl:
                i = starti
                j += int(endl[:-1]) if endl[:-1] else 1

glider = Glyph(name="Glider", x=3, y=3, code="bo$2bo$3o!")
glider_gun = Glyph(
    name="Gosper Gun",
    x=36,
    y=9,
    code="24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o$2o8bo3bob2o4bobo$10bo5bo7bo$11bo3bo$12b2o!",
)
lwss = Glyph(name="LWSS", x=5, y=4, code="bo2bo$o$o3bo$4o!")
mwss = Glyph(name="MWSS", x=6, y=5, code="3bo$bo3bo$o$o4bo$5o!")
hwss = Glyph(name="HWSS", x=7, y=5, code="3b2o$bo4bo$o$o5bo$6o!")
space_rake = Glyph(
    name="Space Rake",
    x=22,
    y=19,
    code="11b2o5b4o$9b2ob2o3bo3bo$9b4o8bo$10b2o5bo2bo2$8bo$7b2o8b2o$6bo9bo2bo$7b5o4bo2bo$8b4o3b2ob2o$11bo4b2o4$18b4o$o2bo13bo3bo$4bo16bo$o3bo12bo2bo$b4o!",
)
time_bomb = Glyph(
    name="Time Bomb", x=15, y=6, code="bo11b2o$obo4bo6bo$7bo4bo$2bo2bo3bo2bo$2b2o6bo$3bo!"
)
glyphs = [glider, glider_gun, lwss, mwss, hwss, space_rake, time_bomb]
num_glyphs = len(glyphs)