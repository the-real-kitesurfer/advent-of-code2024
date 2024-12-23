DAY = "20"

from helper import DEBUG, debug, fetchData
from functools import lru_cache

# Function to find the minimum number of steps
def solveMaze(mat, start, end, invert=False):
  n = len(mat)
  m = len(mat[0])

  visited = [[False for _ in range(m)]
              for _ in range(n)]
  steps = 0

  q = []
  q.append([start[0], start[1]])

  debug(f"Start at {start[0]}, {start[1]} = {mat[start[1]][start[0]]}")

  ar1 = [1, -1, 0, 0]
  ar2 = [0, 0, -1, 1]

  # Loop to run a BFS
  while (len(q) != 0):
    size = len(q)

    steps += 1
    while (size):
      curr = q.pop(0)
      x = curr[0]
      y = curr[1]

      visited[y][x] = True
      for dir in range(0, 4):
        new_y = y + ar1[dir]
        new_x = x + ar2[dir]
        if (new_y >= 0 and new_y < n and new_x >= 0 and new_x < m):
          if ((not invert and not mat[new_y][new_x] == '#') or (invert and mat[new_y][new_x] in ['#', 'S', 'E'])) and not visited[new_y][new_x]:
            debug(f"Step {steps}: {new_x}, {new_y} = {mat[new_y][new_x]}")
            if (new_y == end[1] and new_x == end[0]):
              debug(f"Solved at step {steps}: {new_x}, {new_y} = {mat[new_y][new_x]}")
              return steps
            q.append([new_x, new_y])
            visited[new_y][new_x] = True

      size -= 1
  return -1

def countCheats(maze, minGain, start, end):
  regularDuration = solveMaze(maze, start, end)
  print(f"Regular duration: {regularDuration}")
 
  attempt = 0
  maxAttempts = len(maze) * len(maze[0])

  cnt = 0
  cheats = []
  for x in range(len(maze[0])):
    for y in range(len(maze)):
      if attempt % 1000 == 0:
        print(f"Doint attempt {attempt} - {(100 * attempt) // maxAttempts}% done")
      attempt += 1
      for cheat in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
        cheated = []
        for line in maze:
          row = []
          for c in line:
            row.append(c)
          cheated.append(row)
        if cheated[y][x] == '.':
          cheated[y][x] = '1'
        else:
          continue
        if y+cheat[1] >= len(cheated) or y+cheat[1] == 0 or x+cheat[0] >= len(cheated[0]) or x+cheat[0] <= 0 or (x+cheat[0], y+cheat[1]) in cheats:
          continue
        cheats.append((x, y))
        cheats.append((x+cheat[0], y+cheat[1]))
        if cheated[y+cheat[1]][x+cheat[0]] == '#':
          cheated[y+cheat[1]][x+cheat[0]] = '2'
        else:
          continue
        cheatedDuration = solveMaze(cheated, start, end)
        #print(f"Cheated duration: {cheatedDuration}")
        if regularDuration - cheatedDuration >= minGain:
          print(f"Saved time: {regularDuration - cheatedDuration} for x={x}, y={y} and cheat={cheat}")
          #printMaze(cheated)
          cnt += 1
  return cnt

def countCheats2(maze, minGain, start, end):
  regularDuration = solveMaze(maze, start, end)
  print(f"Regular duration: {regularDuration}")
 
  attempt = 0
  maxAttempts = len(maze) * len(maze[0])

  cnt = 0
  cheats = []
  for x in range(len(maze[0])):
    for y in range(len(maze)):
      if attempt % 1000 == 0:
        print(f"Doing attempt {attempt} - {(100 * attempt) // maxAttempts}% done")
      attempt += 1

      if maze[y][x] == '#':
        continue
      for targetX in range(-20, +21):
        for targetY in range(-20, +21):
          if abs(targetX) + abs(targetY) > 20:
            continue
          cheat = (targetX, targetY)
          if y+cheat[1] >= len(maze) or y+cheat[1] <= 0 or x+cheat[0] >= len(maze[0]) or x+cheat[0] <= 0 or (x, y, x+cheat[0], y+cheat[1]) in cheats:
            continue
          if maze[y+cheat[1]][x+cheat[0]] == '#':
            continue

          cheats.append((x, y, x+cheat[0], y+cheat[1]))

          cheated = []
          for line in maze:
            row = []
            for c in line:
              row.append(c)
            cheated.append(row)

          for i in range(x, targetX):
              cheated[y][x+i] = '.'
          for j in range(y, targetY):
              cheated[y+j][x] = '.'

          durationOfCheat = solveMaze(maze, (x,y), (x+targetX, y+targetY), True)
          if durationOfCheat < abs(targetX) + abs(targetY):
            print(f"durationOfCheat: {durationOfCheat} vs abs(targetX) + abs(targetY) = {abs(targetX) + abs(targetY)}")
            continue

          cheatedDuration = solveMaze(cheated, start, end)
          #print(f"Cheated duration: {cheatedDuration}")
          if regularDuration - cheatedDuration >= minGain:
            print(f"Saved time: {regularDuration - cheatedDuration} for x={x}, y={y} and cheat={cheat}")
            if regularDuration - cheatedDuration == 76:
              printMaze(cheated)
            cnt += 1
  return cnt

def transform(input):
  maze = []
  start = (-1,-1)
  end = (-1,-1)
  for y, row in enumerate(input):
    maze.append(row)
    for x, c in enumerate(row):
      if c == 'S':
        start = (x,y)
      elif c == 'E':
        end = (x,y)

  return maze, start, end

def isTrack(maze, x,y):
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

  maze, start, end = transform(input)
  printMaze(maze)

  if useRealData:
    minGain = 100
  else:
    minGain = 10

  cheatCount = countCheats(maze, minGain, start, end)

  print(f"Result for part 1: {str(cheatCount)}")

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)

  maze, start, end = transform(input)
  printMaze(maze)

  if useRealData:
    minGain = 100
  else:
    minGain = 50

  cheatCount = countCheats2(maze, minGain, start, end)

  print(f"Result for part 2: {str(cheatCount)} - expected 285 for the sample!")

def solve():
  #part1(True)
  part2(False)