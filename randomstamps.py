spacing = 100
samples = 20
size = 2
radius = (1,1)
for i in range(samples):
    for j in range(samples):
        board.randomstamp((i*spacing, j * spacing),radius)
exit()