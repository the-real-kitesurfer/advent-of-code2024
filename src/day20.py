DAY = "20"

from helper import DEBUG, debug, fetchData
from functools import lru_cache

def copyMaze(mat):
  copy = []
  for y, row in enumerate(mat):
    copy.append([])
    for c in row:
      copy[y].append(c)
  return copy

def computeBestPath(previous, endNode):
  nodesOnBestPath = [endNode]
  currentNode = endNode
  while currentNode in previous:
    currentNode = previous[currentNode]
    nodesOnBestPath.append(currentNode)

  step = len(nodesOnBestPath)
  bestPath = {}
  for node in nodesOnBestPath:
    bestPath[node] = step
    step -= 1
  return bestPath

def countCheatsNew(mat, origLength, minGain, distancesStartToEnd, distancesEndToStart):
  # idea: consider all pairs of "." nodes within a max (manhattan) distance of 20 (= the max cheat length)
  # check that the sum of the distance from the start to node 1 + from node 2 to the end is above the "minGain"
  # CHECK: REALLY NEEDED!? compute the best path by _only_ using # tiles
  # remove these temporarily from the maze, compute the new best path
  # and check the minGain is achieved
  uniqueCheats = {}
  numberOfCheatsPerGain = {}
  cheatCount = 0
  start = None
  end = None
  maze = []
  # create list-based clone of mat -> maze
  for y1, row1 in enumerate(mat):
    maze.append([])
    for x1, c1 in enumerate(row1):
      maze[y1].append(c1)

  attempts = 0
  for y1, row1 in enumerate(mat):
    for x1, c1 in enumerate(row1):
      attempts += 1
      if attempts % 1000 == 0: 
        print(f"{attempts}th cheat attempt for {(x1,y1)} ({(100*attempts)//(y1 * len(row1) + x1)}) - found already {cheatCount} cheats")
      
      if c1 == 'S':
        start = (x1,y1)
        #maze[start[1]][start[0]] = '.'
      if c1 == 'E':
        end = (x1,y1)
        #maze[end[1]][end[0]] = '.'

      if not c1 == '#': #need to start on the track
        pt1 = (x1,y1)
        #maze[y1][x1] = 's'
        for y2 in range(y1 - 20, y1 + 21, +1):
          if y2 < 0 or y2 >= len(maze):
            continue
          for x2 in range(x1 - 20 + abs(y1-y2), x1 + 21 - abs(y1-y2), +1):
            if x2 < 0 or x2 >= len(maze[0]):
              continue
            c2 = maze[y2][x2]

            if not c2 == '#': # need to end on the track
              pt2 = (x2,y2)
              if False:
                #maze[y2][x2] = 'e'
                mazeAfterCheating = copyMaze(maze)
                step = 0
                if x1 > x2: dx = -1
                else: dx = +1
                for x in range(x1, x2 + dx, dx):
                  if mazeAfterCheating[y1][x] == '#':
                    mazeAfterCheating[y1][x] = str(step % 10)
                  step += 1
                if y1 > y2: dy = -1
                else: dy = +1
                for y in range(y1+dy, y2 + dy, dy):
                  if mazeAfterCheating[y][x2] == '#' or (y == y2 and not mazeAfterCheating[y][x2] == 'S' and not mazeAfterCheating[y][x2] == 'E'):
                    mazeAfterCheating[y][x2] = str(step % 10)
                  step += 1

                debug(f"Trying to cheat between {pt1} and {pt2}")
                if DEBUG: printMaze(mazeAfterCheating)
                cheatedDistances, endNode, previous = dijkstras(mazeAfterCheating, 'S', 'E', '#')
                newLength = cheatedDistances[endNode]
                if origLength - newLength >= minGain:
                  bestPath = computeBestPath(previous, endNode)
                  # ensure the first and last cheated step are on the best path to avoid detours, and that pt1 comes earlier than pt2
                  if pt1 in bestPath and pt2 in bestPath and bestPath[pt1] < bestPath[pt2]:
                    debug(f"Found cheat that saves {origLength - newLength} picoseconds (taking {newLength} instead of {origLength}), connecting {pt1} and {pt2}")
                    if not (pt1, pt2) in uniqueCheats and not (pt2, pt1) in uniqueCheats:
                      uniqueCheats.append((pt1, pt2))
                      if not origLength - newLength in numberOfCheatsPerGain:
                        numberOfCheatsPerGain[origLength - newLength] = 1
                      else:
                        numberOfCheatsPerGain[origLength - newLength] += 1
                      if origLength - newLength == 60:
                        print(f"Found cheat that saves {origLength - newLength} picoseconds (taking {newLength} instead of {origLength}), connecting {pt1} and {pt2}")
                        printMaze(mazeAfterCheating)

              if True: 
                # no smart computation of cheating at all, just find all pairs of nodes with
                # manhattan distance 20, compute the length from these to start+end and add the distance, and done!
                distToStart = min(distancesStartToEnd[pt1], distancesStartToEnd[pt2])
                distToEnd = min(distancesEndToStart[pt1], distancesEndToStart[pt2])

                cheatDuration = abs(x1 - x2) + abs(y1 - y2)
                newLength = distToStart + cheatDuration + distToEnd
                if origLength - newLength >= minGain:
                  # found cheat
                  debug(f"Found cheat that takes {newLength} instead of {origLength}")
                  if (not pt1 in uniqueCheats or not pt2 in uniqueCheats[pt1]) and (not pt2 in uniqueCheats or not pt1 in uniqueCheats[pt2]):
                    if not pt1 in uniqueCheats:
                      uniqueCheats[pt1] = []
                    uniqueCheats[pt1].append(pt2)
                    cheatCount += 1
                    #uniqueCheats.add((pt1, pt2))
                    if not origLength - newLength in numberOfCheatsPerGain:
                      numberOfCheatsPerGain[origLength - newLength] = 1
                    else:
                      numberOfCheatsPerGain[origLength - newLength] += 1
              # restore maze at pt2
              # maze[y2][x2] = c2

        # restore maze at pt1
        # maze[y1][x1] = c1

  maze[start[1]][start[0]] = 'S'
  maze[end[1]][end[0]] = 'E'
  print(f"Number of cheats per gain: {numberOfCheatsPerGain}")
  return cheatCount #len(uniqueCheats)

        

def dijkstras(mat, startMarker, endMarker, wallMarker):
  unvisited = []
  distances = {}
  previous = {}
  neighbours = {}

  w = len(mat[0])
  h = len(mat)
  
  # add all adjacent, empty nodes in the grid as direct neighbours
  for y, row in enumerate(mat):
    for x, c in enumerate(row):
      if c == startMarker:
        distances[(x,y)] = 0

      if not c == wallMarker:
        unvisited.append((x,y))
        neighbours[(x,y)] = []
        for (dx, dy) in [(-1,0), (+1,0), (0,-1), (0,+1)]:
          if x+dx >= 0 and x+dx < w and y+dy >= 0 and y+dy < h:
            if not mat[y+dy][x+dx] == '#':
              neighbours[(x,y)].append((x+dx, y+dy))

  debug(f"Prepared datastructures for startMarker {startMarker} and endMarker {endMarker}, starting with distances {distances} and unvisited {unvisited}")
  while True:
    # pick unvisited node with smallest distance to start node
    pickedIndex = -1
    picked = None
    debug(f"Picked node is initially {picked}")
    for n, node in enumerate(unvisited):
      debug(f"Checking distance of node {node}")
      if node in distances and (pickedIndex == -1 or distances[node] < distances[picked]):
        picked = node
        pickedIndex = n

    debug(f"Picked node {picked} with distance {distances[picked]}")
    # picked node is the end pos (regardless of direction)
    if mat[picked[1]][picked[0]] == endMarker:
      return distances, picked, previous
    
    # update distances for all neighbours
    debug(f"Updating neighbours of {picked}: {neighbours[picked]}")
    for neighbour in neighbours[picked]:
      if neighbour in unvisited and (neighbour not in distances or distances[neighbour] > distances[picked] + 1):
        distances[neighbour] = distances[picked] + 1
        debug(f"New distance of neighbour {neighbour} is {distances[neighbour]} via {picked}")
        previous[neighbour] = picked
      elif neighbour in unvisited and (distances[neighbour] == distances[picked] + 1):
        debug(f"Neighbour {neighbour} can also be reached from {picked} with same distance, {distances[neighbour]}")

    
    # picked node processed -> remove from list
    #debug(f"Removing {pickedIndex}th element from list of unvisited {len(unvisited)} ...")
    unvisited.pop(pickedIndex)
    if len(unvisited) % 1000 == 0:
      print(f"{len(unvisited)} unvisited nodes")

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

  #cheatCount = countCheats2(maze, minGain, start, end)
  distancesStartToEnd, shortestS2E, previousS2E = dijkstras(maze, 'S', 'E', '#')
  distancesEndToStart, shortestE2S, previousE2S = dijkstras(maze, 'E', 'S', '#')
  print(f"shortestS2E {distancesStartToEnd[shortestS2E]} vs shortestE2S {distancesEndToStart[shortestE2S]}")

  cheatCount = countCheatsNew(maze, distancesStartToEnd[shortestS2E], minGain, distancesStartToEnd, distancesEndToStart)

  print(f"Result for part 2: {str(cheatCount)} - expected 285 for the sample!")

def solve():
  #part1(True)
  part2(True)