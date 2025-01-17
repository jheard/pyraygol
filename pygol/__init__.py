from .Board import Board
from .Glyph import Glyph, GlyphFlip
from .Simulation import Simulation

glyphs = []

glider = Glyph(name="Glider", x=3, y=3, code="bo$2bo$3o!")
glyphs.append(glider)

glider_gun = Glyph(name="Gosper Gun", x=36, y=9,
    code="24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o$2o8bo3bob2o4bobo$10bo5bo7bo$11bo3bo$12b2o!")
glyphs.append(glider_gun)

lwss = Glyph(name="LWSS", x=5, y=4, code="bo2bo$o$o3bo$4o!")
glyphs.append(lwss)
mwss = Glyph(name="MWSS", x=6, y=5, code="3bo$bo3bo$o$o4bo$5o!")
glyphs.append(mwss)
hwss = Glyph(name="HWSS", x=7, y=5, code="3b2o$bo4bo$o$o5bo$6o!")
glyphs.append(hwss)
space_rake = Glyph(
    name="Space Rake",
    x=22,
    y=19,
    code="11b2o5b4o$9b2ob2o3bo3bo$9b4o8bo$10b2o5bo2bo2$8bo$7b2o8b2o$6bo9bo2bo$7\
b5o4bo2bo$8b4o3b2ob2o$11bo4b2o4$18b4o$o2bo13bo3bo$4bo16bo$o3bo12bo2bo$b4o!",
)
glyphs.append(space_rake)
time_bomb = Glyph(
    name="Time Bomb", x=15, y=6, code="bo11b2o$obo4bo6bo$7bo4bo$2bo2bo3bo2bo$2b2o6bo$3bo!"
)
glyphs.append(time_bomb)
#N Cord puller
#O Dean Hickerson
#C A sawtooth with expansion factor 6 that was found on May 14, 1991.
#C www.conwaylife.com/wiki/index.php?title=Cord_puller
cord_puller = Glyph(name = "Cord Puller", x = 98, y = 93, rule = "b3/s23",
                    code = "28b3o67b$27bo3bo66b$26bo4bo8b2o3b3o50b$26bo2bobo7b4o55b$26b2obobo6bo3b2o54b$28b2obo2bo4b2obobo53b$18b3o9b2o2bo63b$17bo2bo10b3o13bo6b2o42b$16bo4bo22bo2bo6bo43b$16bo2b3o23b3o50b$16bo5bo75b$17b7o74b$23bo74b$23bo74b$21b2o75b$62b2o34b$62bo35b2$24b3obo69b$24b3obo69b$25bo8b2o62b$26bo3b3ob2o62b$27bo6bo63b$28bobobobo35b2o26b$29bo40bo9bo17b$61bo16b3o17b$2b3o55bobo14bo20b$bo3bo53b2ob2o13b2o19b$o4bo53b2ob2o34b$o2bobo52b3o37b$2obobo52b3o3bo33b$2b2obo2bo50b2o37b$4b2o2bo50bobo36b$5b3o64b2o3b2o19b$72bobobobo19b$73b5o20b$74b3o21b$75bo22b3$47b2o49b$45b6o47b$44b6o48b$43bo6bo26b2o19b$44b3o30bo20b$8b2o35b2o31b3o17b$8bo39bo8bo22bo17b$53b2o2b2ob3o35b$53bo5b4o35b$57b2o39b2$35bo15bo29bo2bo13b$34bobo12b3o28bo3b2o2b2o8b$16b2o15b2ob2o10bo31bo7bo9b$16bo16b2ob2o10b2o19bo11b4o8b2o3b$32b3o32b3o23bo4b$32b3o3bo27bo12bo18b$33b2o31b2o3bo6b2o18b$33bobo35b3o4bobo17b$74bo23b$73b2o23b$24b2o17b2o3b2o48b$24bo27b3o43b$43bo5bo4bo6b2o3b2o30b$53bo8b5o31b$44b2ob2o14b3o32b$46bo17bo8b2o3b2o12b5ob$58b3o12bo5bo11bob3obo$58bo33bo3bob$48bo10bo14bo3bo14b3o2b$47bobo25b3o16bo3b$46bo3bo41b2o4b$46b5o40bobo4b$45b2o3b2o39bobo4b$46b5o41bo5b$47b3o11b3o34b$48bo49b$61bobo14bo10b2obob2o2b$60b5o11b2ob2o8bo5bo2b$59b2o3b2o24bo3bo3b$59b2o3b2o9bo5bo9b3o4b2$75b2o3b2o16b3$48b2o48b$48bo49b2$61b2o28b2o5b$61bo29bo6b2$78b2o18b$78bo!" )
glyphs.append(cord_puller)



num_glyphs = len(glyphs)