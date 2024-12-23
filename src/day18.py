DAY = "18"

from helper import DEBUG, debug, fetchData
from functools import lru_cache

# Function to find the minimum number of steps
def solveMaze(mat):
  n = len(mat)
  m = len(mat[0])
  if (n == 1 and m == 1 and (mat[0][0] == 0)):
	  return 0

  visited = [[False for _ in range(m)]
              for _ in range(n)]
  steps = 0

  q = []
  q.append([0, 0])

  ar1 = [1, -1, 0, 0]
  ar2 = [0, 0, -1, 1]

  # Loop to run a BFS
  while (len(q) != 0):
    size = len(q)

    steps += 1
    while (size):
      curr = q.pop(0)
      i = curr[0]
      j = curr[1]

      visited[i][j] = True
      for dir in range(0, 4):
        new_x = i + ar1[dir]
        new_y = j + ar2[dir]
        if (new_x >= 0 and new_x < n and new_y >= 0 and new_y < m):
          if (mat[new_x][new_y] == '.' and (not visited[new_x][new_y])):
            if (new_x == n - 1 and new_y == m - 1):
              return steps
            q.append([new_x, new_y])
            visited[new_x][new_y] = True

      size -= 1
  return -1

def transform(input, bits, width, height):
  maze = []
  for y in range(height+1):
    row = []
    for x in range(width+1):
      row.append('.')
    maze.append(row)

  for i in range(bits):
    bit = input[i]
    x,y = bit.split(',')
    maze[int(y)][int(x)] = '#'
  
  return maze

def isFree(maze, x,y):
  #debug(f"Is valid for {reindeer}: {reindeer[0] >= 0 and reindeer[0] < len(maze[0]) and reindeer[1] >= 0 and reindeer[1] < len(maze) and not maze[reindeer[1]][reindeer[0]] == '#'}")
  return x >= 0 and x < len(maze[0]) and y >= 0 and y < len(maze) and not maze[y][x] == '#'

def shortestPath(maze, x,y, destX, destY, oldVisited):
  if x == len(maze[0]) - 1 and y == len(maze) - 1:
    print("Reached goal!")
    return 0

  visited = []
  for visit in oldVisited:
    visited.append(visit)

  if (x, y) in visited:
    return -1
  visited.append((x, y))

  #if len(visited) > 100:
  #  print(f"Giving up after {len(visited)} visits.")
  #  return -1
  debug(f"Bit: {x}, {y}, #visits: {len(visited)}")
  #debug(f"Reindeer: {reindeer}, visited: {visited}")

  paths = []
  for deltaX,deltaY in [(-1,0), (+1,0), (0,-1), (0,+1)]:
    if isFree(maze, x+deltaX, y+deltaY):
      length = 1 + shortestPath(maze, x+deltaX, y+deltaY, destX, destY, visited)
      if length > 0:
        paths.append(length)

  shortest = -1
  if len(paths) > 0:
    print(f"Found {len(paths)} paths.")
  for path in paths:
    if shortest == -1 or path < shortest:
      print(f"Found path {path}, shortest {shortest}")
      shortest = path
  debug(f"Returning {shortest}")
  return shortest

def printMaze(maze):
  print("---")
  for row in maze:
    line = ""
    for x in range(len(row)):
        line += str(row[x])
    print(line)
  print("---")


def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)

  if useRealData:
    bits, width, height = (1024,70,70)
  else:
   bits, width, height = (0*12,6,6)

  maze = transform(input, bits, width, height)
  printMaze(maze)

  pathLength = solveMaze(maze)

  print(f"Result for part 1: {str(pathLength)}")

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  pathLength = 1
  bits = 0
  while pathLength > 0:
    input = fetchData(DAY, useRealData)

    if useRealData:
      width, height = (70,70)
    else:
      bits, width, height = (0*12,6,6)

    maze = transform(input, bits, width, height)
    #printMaze(maze)

    pathLength = solveMaze(maze)
    print(f"Maze solvable for first bits {bits} with min. pathlength {str(pathLength)}")
    bits += 1

  print(f"Result for part 2: {str(input[bits-2])}")

def solve():
  #part1(True)
  part2(True)

