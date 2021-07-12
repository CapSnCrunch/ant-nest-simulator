import pygame
import numpy as np
import matplotlib.pyplot as plt
from pygame.constants import MOUSEBUTTONDOWN
from classes import Ant, Wall, SFZ, Colony

K1, K2 = 50, 50
N = 250
config = 'RID' # RM, RID, AID
time_steps = 500
dt = 1
scale = 10

print('SHD max:', N*(K1*K2-N)/(K1*K2)**2)

# TODO Functions
# Find the center of SFZ
# Find the area of a union of rectangles

if __name__ == '__main__':
    # Start a new pygame window
    run = True
    start = None
    update = False
    win = pygame.display.set_mode((K1 * scale, K2 * scale))
    pygame.display.set_caption('Ant Nest Simulator')

    # Define SFZs
    sfzs = []
    colors = [(200, 0, 0), (200, 200, 0), (0, 200, 0), (0, 0, 200)]
    for n in range(3):
        i, j = np.random.randint(K1), np.random.randint(K2)
        sfzs.append(SFZ([(x,y) for x in range(i, i+3) for y in range(j, j+3)], colors[n]))

    f = [0.98, 0.8, 0.6, 0.4, 0.2]
    colonies = [Colony(K1, K2, N, f[i], sfzs = sfzs, config = config) for i in range(5)]
    
    t = 0
    clock = pygame.time.Clock()
    while run:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not update:
                cursor = list(pygame.mouse.get_pos())
                start = (cursor[0] // scale, cursor[1] // scale)
            elif event.type == pygame.MOUSEBUTTONUP and not update:
                cursor = list(pygame.mouse.get_pos())
                stop = (cursor[0] // scale + (cursor[0] // scale >= start[0]), cursor[1] // scale + (cursor[1] // scale >= start[1]))
                for colony in colonies:
                    colony.set_wall(start, stop)
                start = None
            elif event.type == pygame.KEYDOWN:
                update = True
                for colony in colonies:
                    if colony.ants == []:
                        colony.create_ants()

        colonies[0].draw(win, scale)
        if start != None:
            cursor = list(pygame.mouse.get_pos())
            i, j = min(start[0], cursor[0] // scale), min(start[1], cursor[1] // scale)
            w, h = abs(cursor[0] // scale - start[0]) + (cursor[0] // scale >= start[0]), abs(cursor[1] // scale - start[1]) + (cursor[1] // scale >= start[1])
            pygame.draw.rect(win, (100, 100, 100), (i*scale, j*scale, w*scale, h*scale), 2)
            pygame.display.update()
            
        if update:
            for colony in colonies:
                colony.update()
            t += 1
            if t == time_steps:
                run = False

    SHDs = [colony.shd for colony in colonies]
    C = [colony.contacts for colony in colonies]
    R = np.array([(C[0][i+1]-C[0][i])/dt for i in range(len(C[0])-1)])
    #I = C / N

    # Spatial Fidelity of each task group
    '''for p in range(colony.P):
        print('SF('+str(p)+'):', colony.get_sf(p))'''

    plot = plt.figure(1)
    legend = []
    for i in range(len(SHDs)):
        plt.plot(SHDs[i])
        legend.append('SF:' + str(colonies[i].f))
    plt.title(config)
    plt.legend(legend)
    plt.xlabel('t')
    plt.ylabel('SHD')

    '''plot2 = plt.figure(2)
    plt.plot(I)
    plt.title('Proportion of Informed Ants')
    plt.xlabel('t')
    plt.ylabel('I(t)')

    plot3 = plt.figure(3)
    plt.scatter(np.arange(len(R)), R, s = 3)
    plt.title('Contact Rate')
    plt.xlabel('t')
    plt.ylabel('C(t) - C(t-dt)')'''

    plt.show()