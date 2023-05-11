import numpy as np
import time




def gs(i, j, startx, starty):
    return abs(i - startx) + abs(j - starty)
def h1(i, j, endx, endy):
    return 10*(abs(i - endx) + abs(j - endy))
def h2(i, j, endx, endy):
    return pow(i - endx, 2) + pow(j - endy, 2)

#startx, starty, endx, endy=map(int, input().split())#

def A(b, startx, starty, endx, endy):
    a = 1 - b
    r = a.shape().first
    c = a.shape().second
    for i in range(0, r):
        for j in range(0, c):
            if a[i][j] != 0 and a[i][j] != 1:
                a[i][j] = 0
    if a[startx - 1, starty - 1] == 1:
        return -1
    else:
        Close = [[startx, starty]]
        Opens = [[startx, starty]]
        crossings = []
        road = 100
        rows, cols = a.shape
        while True:
            if Close[-1] != [endx, endy]:
                Open = []
                i, j = Close[-1][0] - 1, Close[-1][1] - 1
                for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1), (i + 1, j + 1), (i + 1, j - 1), (i - 1, j + 1), (i - 1, j - 1)]:
                    if [ni + 1, nj + 1] not in Opens and 0 <= ni < rows and 0 <= nj < cols and a[ni, nj] == 0:
                        Open.append([ni + 1, nj + 1])
                a[i, j] = road
                road = road + 1
                if Open:
                    Open = sorted(Open, key=lambda x: gs(x[0], x[1]) + h2(x[0], x[1]), reverse=True)
                    Opens.extend(Open)
                    Close.append(Open.pop())
                    if Open:
                        crossings.extend(Open)
                elif crossings:
                    next_way = crossings.pop()
                    road -= 1
                    Close.pop()
                    Close.append(next_way)
                else:
                    break
            else:
                a[endx - 1, endy - 1] = road
                break

        size = Close.size()
        if size > 10 :
            size = 10
        ans1 = np.array(Close[0:size - 1])
        ans2 = np.array(Close[1:size])
        ans = ans2 - ans1
        return ans


def generate_maze(width, height, wall_density):
    # Initialize the maze with walls
    maze = [[0] * width for _ in range(height)]

    # Initialize the visited set
    visited = set()

    # Set the starting cell to (0, 0)
    x, y = 0, 0
    visited.add((x, y))

    # Initialize the frontier list
    frontier = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if
                0 <= x + dx < width and 0 <= y + dy < height]

    # Loop until all cells have been visited
    while frontier:
        # Choose a random frontier cell
        x, y = random.choice(frontier)
        frontier.remove((x, y))

        # Choose a random visited neighbor
        nx, ny = random.choice(
            [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if (x + dx, y + dy) in visited])

        # Add a passage with probability (1 - wall_density)
        if random.random() < 1 - wall_density:
            maze[y][x] = 1
            visited.add((x, y))

            # Add unvisited neighbors to the frontier
            frontier.extend([(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if
                             0 <= x + dx < width and 0 <= y + dy < height and (x + dx, y + dy) not in visited and (
                             x + dx, y + dy) not in frontier])

    # Ensure that there is a solution from (0, 0) to (width - 1,height - 1)
    maze[height - 1][width - 1] = 1

    trapcnt = 0_
    trapnum = width * height * wall_density * wall_density
    while trapcnt < trapnum:
        x = random.randint()
        y = random.randint()
        if(maze[x][y] == 1):
            maze[x][y] = 8
            trapcnt += 1

    return maze


