DAY = "16"

from helper import DEBUG, debug, fetchData
from functools import lru_cache

maze = []

def transform(input):
  global maze
  maze = []
  startPos = (-1,-1,'>')
  endPos = (-1,-1,'?')
  for y,line in enumerate(input):
    for x,c in enumerate(line):
      if c == 'S':
        startPos = (x, y, '>')
      if c == 'E':
        endPos = (x, y, '?')
    maze.append(line)
  return startPos, endPos

def dijkstras(start):
  unvisited = []
  weights = {}
  distances = {start: 0}
  previous = {}
  neighbours = {}
  # initialize list of univisited nodes with reindeers at any valid position
  for y in range(len(maze)):
    for x in range(len(maze[0])):
      if not maze[y][x] == '#':
        for dir in ['>','v', '<', '^']:
          reindeer = (x, y, dir)
          unvisited.append(reindeer)
          neighbours[reindeer] = []
          for t in [-90, 0, +90]:
            if t == 0:
              updatedReindeer = move(reindeer)
              if isValid(updatedReindeer):
                weights[reindeer, updatedReindeer] = 1
                neighbours[reindeer].append(updatedReindeer)
            elif t == -90:
              updatedReindeer = turn(reindeer, True)
              if isValid(updatedReindeer):
                weights[reindeer, updatedReindeer] = 1000
                neighbours[reindeer].append(updatedReindeer)
            else:
              updatedReindeer = turn(reindeer, False)
              if isValid(updatedReindeer):
                weights[reindeer, updatedReindeer] = 1000
                neighbours[reindeer].append(updatedReindeer)

  debug(f"Prepared datastructures, starting with distances {distances} and unvisited {unvisited}")
  while True:
    # pick unvisited node with smallest distance to start node
    pickedIndex = -1
    picked = None
    #debug(f"Picked node is initially {picked}")
    for n, node in enumerate(unvisited):
      #debug(f"Checking distance of node {node}")
      if node in distances and (pickedIndex == -1 or distances[node] < distances[picked]):
        picked = node
        pickedIndex = n

    debug(f"Picked node {picked} with distance {distances[picked]}")
    # picked node is the end pos (regardless of direction)
    if maze[picked[1]][picked[0]] == 'E':
      return distances[picked], previous
    
    # update distances for all neighbours
    debug(f"Updating neighbours of {picked}: {neighbours[picked]}")
    for neighbour in neighbours[picked]:
      if neighbour in unvisited and (neighbour not in distances or distances[neighbour] > distances[picked] + weights[picked, neighbour]):
        distances[neighbour] = distances[picked] + weights[picked, neighbour]
        debug(f"New distance of neighbour {neighbour} is {distances[neighbour]} via {picked}")
        previous[neighbour] = [picked] # remove old entries in previous, the new path is shorter!
      elif neighbour in unvisited and (distances[neighbour] == distances[picked] + weights[picked, neighbour]):
        debug(f"Neighbour {neighbour} can also be reached from {picked} with same distance, {distances[neighbour]}")
        previous[neighbour].append(picked)
      if neighbour in [(15, 1, '^'), (15, 2, '^')]:
        print(f"Previous for {neighbour}: {previous[neighbour]}; processing {picked}")

    
    # picked node processed -> remove from list
    #debug(f"Removing {pickedIndex}th element from list of unvisited {len(unvisited)} ...")
    unvisited.pop(pickedIndex)
    if len(unvisited) % 1000 == 0:
      print(f"{len(unvisited)} unvisited nodes")


@lru_cache(maxsize=None)
def isValid(reindeer):
  #debug(f"Is valid for {reindeer}: {reindeer[0] >= 0 and reindeer[0] < len(maze[0]) and reindeer[1] >= 0 and reindeer[1] < len(maze) and not maze[reindeer[1]][reindeer[0]] == '#'}")
  return reindeer[0] >= 0 and reindeer[0] < len(maze[0]) and reindeer[1] >= 0 and reindeer[1] < len(maze) and not maze[reindeer[1]][reindeer[0]] == '#'

@lru_cache(maxsize=None)
def canTurn(reindeer):
  turnLeftAndMove = move(turn(reindeer, True))
  if isValid(turnLeftAndMove):
    return True

  turnRightAndMove = move(turn(reindeer, False))
  if isValid(turnRightAndMove):
    return True

  return False

@lru_cache(maxsize=None)
def move(reindeer):
  if reindeer[2] == '<':
    return (reindeer[0]-1,reindeer[1],reindeer[2])
  if reindeer[2] == '>':
    return (reindeer[0]+1,reindeer[1],reindeer[2])
  if reindeer[2] == '^':
    return (reindeer[0],reindeer[1]-1,reindeer[2])
  if reindeer[2] == 'v':
    return (reindeer[0],reindeer[1]+1,reindeer[2])

@lru_cache(maxsize=None)
def turn(reindeer,left):
  if left:
    if reindeer[2] == '<':
      return (reindeer[0],reindeer[1],'v')
    if reindeer[2] == 'v':
      return (reindeer[0],reindeer[1],'>')
    if reindeer[2] == '>':
      return (reindeer[0],reindeer[1],'^')
    if reindeer[2] == '^':
      return (reindeer[0],reindeer[1],'<')
  else:
    if reindeer[2] == '<':
      return (reindeer[0],reindeer[1],'^')
    if reindeer[2] == '^':
      return (reindeer[0],reindeer[1],'>')
    if reindeer[2] == '>':
      return (reindeer[0],reindeer[1],'v')
    if reindeer[2] == 'v':
      return (reindeer[0],reindeer[1],'<')


def shortestPath(reindeer, oldVisited, turned, recDepth):
  debug(f"Calling shortestPath with recursion depth {recDepth}")
  visited = []
  for visit in oldVisited:
    visited.append(visit)

  if len(visited) > 140*140 or recDepth > 500:
    debug(f"Giving up after {len(visited)} visits and with recurion depth {recDepth}")
    return -1

  debug(f"Reindeer: {reindeer}, #visits: {len(visited)}")
  debug(f"Reindeer: {reindeer}, visited: {visited}")

  if not turned:
    if (reindeer[0], reindeer[1]) in visited:
      debug(f"Visited {reindeer} already. BREAK")
      return -1
    visited.append((reindeer[0], reindeer[1]))

  if maze[reindeer[1]][reindeer[0]] == 'E':
    print(f"Reached end! with {len(visited)} visits. DONE")
    return 0

  moves = 0    
  while not canTurn(reindeer) and isValid(move(reindeer)):
    debug(f"Reindeer {reindeer} cannot turn, moving to {move(reindeer)}")
    moves += 1
    reindeer = move(reindeer)
    visited.append((reindeer[0], reindeer[1]))
    turned = False
    if maze[reindeer[1]][reindeer[0]] == 'E':
      print(f"Reached end! with {len(visited)} visits. DONE")
      return moves

  paths = []
  newPos = move(reindeer)
  if isValid(newPos):
    additionalPath = shortestPath(newPos, visited, False, recDepth + 1)
    if additionalPath >= 0:
      paths.append(moves + 1 + additionalPath)

  if not turned:
    newPos = turn(reindeer,True)
    if isValid(newPos):
      additionalPath = shortestPath(newPos, visited, True, recDepth + 1)
      if additionalPath >= 0:
        paths.append(moves + 1000 + additionalPath)

    newPos = turn(reindeer,False)
    if isValid(newPos):
      additionalPath = shortestPath(newPos, visited, True, recDepth + 1)
      if additionalPath >= 0:
        paths.append(moves + 1000 + additionalPath)
  
  shortest = -1
  #if len(paths) > 0:
  debug(f"Found {len(paths)} paths via {visited}.")
  for path in paths:
    if shortest == -1 or path < shortest:
      debug(f"Found path {path}, shortest {shortest}")
      shortest = path
  print(f"Returning {shortest}")
  return shortest

def shortestPathWithoutRecursion(options):
  #debug(f"Calling shortestPath with these options: {options}")

  bestOption = -1
  for i, option in enumerate(options):
    if bestOption == -1 or option[3] < options[bestOption][3]:
      bestOption = i
  reindeer, oldVisited, turned, score = options.pop(bestOption)
  print(f"Calling shortestPath with {len(options)} options, best has score {score}")

  visited = []
  for visit in oldVisited:
    visited.append(visit)

  if len(visited) > 140*140:
    debug(f"Giving up after {len(visited)} visits")
    return -1

  debug(f"Reindeer: {reindeer}, #visits: {len(visited)}")
  debug(f"Reindeer: {reindeer}, visited: {visited}")

  if not turned:
    if (reindeer[0], reindeer[1]) in visited:
      debug(f"Visited {reindeer} already. BREAK")
      return -1
    visited.append((reindeer[0], reindeer[1]))

  if maze[reindeer[1]][reindeer[0]] == 'E':
    print(f"Reached end! with {len(visited)} visits. DONE")
    return score

  moves = 0    
  while not canTurn(reindeer) and isValid(move(reindeer)):
    debug(f"Reindeer {reindeer} cannot turn, moving to {move(reindeer)}")
    moves += 1
    reindeer = move(reindeer)
    visited.append((reindeer[0], reindeer[1]))
    turned = False
    if maze[reindeer[1]][reindeer[0]] == 'E':
      print(f"Reached end! with {len(visited)} visits. DONE")
      return moves + score

  paths = []
  newPos = move(reindeer)
  if isValid(newPos):
    options.append((newPos, visited, False, score + moves + 1))

  if not turned:
    newPos = turn(reindeer,True)
    if isValid(newPos):
      options.append((newPos, visited, True, score + moves + 1000))

    newPos = turn(reindeer,False)
    if isValid(newPos):
      options.append((newPos, visited, True, score + moves + 1000))

  return -1

@lru_cache(maxsize=None)
def minPathLength(reindeer, endPos):
  if endPos[0] == reindeer[0] and endPos[1] == reindeer[1]:
    return 0 # already solved ;-)
  else:
    xScore = 0
    if reindeer[2] == '^' or reindeer[2] == 'v':
      xScore = 1000 + abs(endPos[0] - reindeer[0]) # need to turn 1x left/right
    elif (reindeer[2] == '<' and endPos[0] <= reindeer[0]) or (reindeer[2] == '>' and endPos[0] >= reindeer[0]):
      xScore = abs(reindeer[0] - endPos[0]) # need to move left/right
    elif (reindeer[2] == '<' and endPos[0] > reindeer[0]) or (reindeer[2] == '>' and endPos[0] < reindeer[0]):
      xScore = 1000 + abs(reindeer[0] - endPos[0]) # direction is wrong -> need to turn at least twice

    yScore = 0
    if reindeer[2] == '<' or reindeer[2] == '>':
      yScore =  1000 + abs(endPos[1] - reindeer[1]) # need to turn 1x up/down
    elif (reindeer[2] == '^' and endPos[1] <= reindeer[1]) or (reindeer[2] == 'v' and endPos[1] >= reindeer[1]):
      yScore =  abs(reindeer[1] - endPos[1]) # need to move up/down
    elif (reindeer[2] == 'v' and endPos[1] > reindeer[1]) or (reindeer[2] == '^' and endPos[1] < reindeer[1]):
      yScore = 1000 + abs(reindeer[1] - endPos[1]) # y-value already correct, but direction is wrong -> need to turn at least twice

  return xScore + yScore

def shortestPathViaList(startPos, endPos):
  optionsByMinimumLength = {}
  optionsByMinimumLength[minPathLength(startPos, endPos)] = [(startPos, [startPos], 0, False)]
  shortestMinPathLength = 0
  while True:
    #shortestMinPathLength = 0
    while True:
      if shortestMinPathLength in optionsByMinimumLength and len(optionsByMinimumLength[shortestMinPathLength]) > 0:
        break
      shortestMinPathLength += 1

    #print(f"Shortest min path length: {shortestMinPathLength}")
    option = optionsByMinimumLength[shortestMinPathLength].pop()
    reindeer, oldVisited, score, turned = option
    visited = []
    for visit in oldVisited:
      visited.append(visit)
    print(f"Shortest min path length: {shortestMinPathLength}, #visits: {len(visited)}, score: {score}, reindeer: {reindeer}")

    debug(f"Reindeer: {reindeer}, #visits: {len(visited)}")
    #debug(f"Reindeer: {reindeer}, visited: {visited}")

    if not turned:
      if (reindeer[0], reindeer[1]) in visited:
        debug(f"Visited {reindeer} already. BREAK")
        continue
      visited.append((reindeer[0], reindeer[1]))

    if maze[reindeer[1]][reindeer[0]] == 'E':
      print(f"Reached end! with {len(visited)} visits and score {score}. Visited: {visited}")
      return score
      
    paths = []
    newPos = move(reindeer)
    if isValid(newPos):
      minLen = score + 1 + minPathLength(newPos, endPos)
      if not minLen in optionsByMinimumLength:
        optionsByMinimumLength[minLen] = []
      optionsByMinimumLength[minLen].append((newPos, visited, score + 1, False))

    if not turned:
      newPos = turn(reindeer,True)
      if isValid(newPos):
        minLen = score + 1000 + minPathLength(newPos, endPos)
        if not minLen in optionsByMinimumLength:
          optionsByMinimumLength[minLen] = []
        optionsByMinimumLength[minLen].append((newPos, visited, score + 1000, True))

      newPos = turn(reindeer,False)
      if isValid(newPos):
        minLen = score + 1000 + minPathLength(newPos, endPos)
        if not minLen in optionsByMinimumLength:
          optionsByMinimumLength[minLen] = []
        optionsByMinimumLength[minLen].append((newPos, visited, score + 1000, True))
    

def printTiles(tiles):
  print("-- TOP --")
  for y, row in enumerate(maze):
    line = ""
    for x, c in enumerate(row):
      if (x,y) in tiles:
        line += '0'
      else:
        line += c
    print(f"{line}")
  print("--BOTTOM --")


def findBestPaths(previous, endPos):
  bestPaths = []
  for posAndDir in previous.keys():
    print(f"Comparing {posAndDir} to {endPos}")
    if (posAndDir[0], posAndDir[1]) == (endPos[0], endPos[1]):
      bestPaths.append(posAndDir)
      break
  processed = []
  print(f"Starting with {bestPaths}")
  while True:
    unchanged = True
    for posAndDir in bestPaths:
      if not posAndDir in processed:
        print(f"Processed {posAndDir}")
        processed.append(posAndDir)
        unchanged = False

        if posAndDir in previous:
          for prevPosAndDir in previous[posAndDir]:
            if not prevPosAndDir in bestPaths:
              bestPaths.append(prevPosAndDir)
    if unchanged:
      return bestPaths

def findTilesOnBestPaths(reindeer, bestLength):
    debug(f"Checking {reindeer}, {bestLength} left to spend")
    tilesOnBestPaths = []
    if bestLength < 0 or not isValid(reindeer):
      return tilesOnBestPaths

    tilesOnBestPaths.append(reindeer)
    if maze[reindeer[1]][reindeer[0]] == 'E':
      print(f"Reached the end with {reindeer}, {bestLength} budget left")
      return tilesOnBestPaths

    reindeerMoved = move(reindeer)
    newTilesOnBestPaths = findTilesOnBestPaths(reindeerMoved, bestLength - 1)
    for tile in newTilesOnBestPaths:
      if not tile in tilesOnBestPaths:
        tilesOnBestPaths.append(tile)

    reindeerTurnedLeft = turn(reindeer, True)
    newTilesOnBestPaths = findTilesOnBestPaths(reindeerTurnedLeft, bestLength - 1000)
    for tile in newTilesOnBestPaths:
      if not tile in tilesOnBestPaths:
        tilesOnBestPaths.append(tile)

    reindeerTurnedRight = turn(reindeer, False)
    newTilesOnBestPaths = findTilesOnBestPaths(reindeerTurnedRight, bestLength - 1000)
    for tile in newTilesOnBestPaths:
      if not tile in tilesOnBestPaths:
        tilesOnBestPaths.append(tile)

    if len(tilesOnBestPaths) > 1:
      return tilesOnBestPaths
    else:
      return []

def countUniqueTiles(tilesOnBestPath):
  uniqueTiles = []
  for dirAndPos in tilesOnBestPath:
    if not (dirAndPos[0], dirAndPos[1]) in uniqueTiles:
      uniqueTiles.append((dirAndPos[0], dirAndPos[1]))
  return uniqueTiles

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)
  startingPos, endPos = transform(input)

  pathLength, _ = dijkstras(startingPos)

  print(f"Result for part 1: {str(pathLength)} (expected: 7036 for the small and 11048 for the large exampkle)")

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)
  startPos, endPos = transform(input)

  # idea: start from start, and take any valid path WHILE the distance is below the minimal one ....
  pathLength, visited = dijkstras(startPos)

  print(f"pathLength: {pathLength}, len(visited): {len(visited)}")
  tilesOnBestPath = findBestPaths(visited, endPos)
  #tilesOnBestPath = findTilesOnBestPaths(startPos, 0*7036+1*11048+0*72428)
  uniqueTiles = countUniqueTiles(tilesOnBestPath)
  printTiles(uniqueTiles)

  print(f"Result for part 2: {str(len(uniqueTiles))} (expected 45 for the small and 64 for the large example)")

def solve():
  #part1(False)
  part2(True)