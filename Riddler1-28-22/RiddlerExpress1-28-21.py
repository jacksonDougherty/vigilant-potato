from pickletools import uint8
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation

def simulateLife(N, generations):
    # Compute the middle index for given grid size N
    halfN = N // 2

    initialGrid = np.zeros((N, N), np.uint8)
    # Set up the initial condtions
    initialGrid[halfN, (halfN-1):(halfN+2)]=255
    initialGrid[(halfN-1):(halfN+2), halfN]=255

    def cellAlive(grid, gridCopy, i, j):

        if grid[i, j] == 255:
            # Without overpopulation, a live cell cannot die, so we do not need to check its neighbors
            pass
        else:
            # This total uses periodic boundary conditions for simplicity
            # If life gets to the boundary, then we should increase the initial grid size N
            '''
            total = (grid[(i -1)%N , (j-1)%N] + grid[(i-1)%N, j] + grid[(i-1)%N, (j+1)%N] + 
                    grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                    grid[(i-1)%N, (j+1)%N] + grid[i, (j+1)%N] + grid[(i+1)%N, (j+1)%N])
            '''
            total = (int(grid[(i -1)%N , (j-1)%N]) + int(grid[(i-1)%N, j]) + int(grid[(i-1)%N, (j+1)%N]) + 
                    int(grid[i, (j-1)%N]) + int(grid[i, (j+1)%N]) +
                    int(grid[(i+1)%N, (j-1)%N]) + int(grid[(i+1)%N, j]) + int(grid[(i+1)%N, (j+1)%N]))
            
            if total/255 > 3:
                # In this modified Game of Life, there is no overpopulation
                gridCopy[i, j] = 255
            elif total/255 == 3:
                gridCopy[i, j] = 255
            else:
                # Without overpopulation, a once living cell cannot die, and so its neighbors cannot die either
                # With overpopulation, we should set grid[i,j]=0
                pass
            
    def updateLife(frame, img, grid, ax):

        gridCopy = grid.copy()

        for i in range(N):
            for j in range(N):
                cellAlive(grid, gridCopy, i, j)

        # Replace the grid with its copy
        grid[:] = gridCopy[:]

        img.set_data(grid)
        # Frame numbers give incorrect generation for first two generations
        ax.set_title("Generation " + str(frame+3) + " has " + str(int(np.sum(grid)/255)) + " cells")
        # Frame 7 corresponds to generaion 10 in the riddler's numbering
        if frame == 7: 
            print(np.sum(grid)/255)
        return [img]



    fig, ax = plt.subplots()
    img = ax.imshow(initialGrid)
    anim = FuncAnimation(fig, updateLife, fargs=(img, initialGrid, ax), 
                        frames = generations, interval = 1000,
                        blit=False, repeat=False)
    plt.show()


simulateLife(21, 8)
#simulateLife(80, 60)
# Repeat on the animation does not work with this setup because the grid object does not reset
# Also, the image might be nicer with grid lines visible. 