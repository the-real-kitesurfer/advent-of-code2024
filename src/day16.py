DAY = "16"

from helper import DEBUG, debug, fetchData
from functools import lru_cache

maze = []

def transform(input):
  startPos = (-1,-1)
  endPos = (-1,-1)
  for y,line in enumerate(input):
    for x,c in enumerate(line):
      if c == 'S':
        startPos = (x,y)
      if c == 'E':
        endPos = (x,y)
    maze.append(line)
  return startPos, endPos

@lru_cache(maxsize=None)
def isValid(reindeer):
  debug(f"Is valid for {reindeer}: {reindeer[0] >= 0 and reindeer[0] < len(maze[0]) and reindeer[1] >= 0 and reindeer[1] < len(maze) and not maze[reindeer[1]][reindeer[0]] == '#'}")
  return reindeer[0] >= 0 and reindeer[0] < len(maze[0]) and reindeer[1] >= 0 and reindeer[1] < len(maze) and not maze[reindeer[1]][reindeer[0]] == '#'

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


def shortestPath(reindeer, oldVisited, turned):
  visited = []
  for visit in oldVisited:
    visited.append(visit)

  if len(visited) > 100:
    print(f"Giving up after {len(visited)} visits.")
    return -1
  debug(f"Reindeer: {reindeer}, #visits: {len(visited)}")
  #debug(f"Reindeer: {reindeer}, visited: {visited}")

  if not turned:
    if (reindeer[0], reindeer[1]) in visited:
      debug(f"Visited {reindeer} already. BREAK")
      return -1
    visited.append((reindeer[0], reindeer[1]))

  if maze[reindeer[1]][reindeer[0]] == 'E':
    print(f"Reached end! with {len(visited)} visits. DONE")
    return 0
    
  paths = []
  newPos = move(reindeer)
  if isValid(newPos):
    additionalPath = shortestPath(newPos, visited, False)
    if additionalPath >= 0:
      paths.append(1 + additionalPath)

  if not turned:
    newPos = turn(reindeer,True)
    if isValid(newPos):
      additionalPath = shortestPath(newPos, visited, True)
      if additionalPath >= 0:
        paths.append(1000 + additionalPath)

    newPos = turn(reindeer,False)
    if isValid(newPos):
      additionalPath = shortestPath(newPos, visited, True)
      if additionalPath >= 0:
        paths.append(1000 + additionalPath)
  
  shortest = -1
  if len(paths) > 1:
    print(f"Found {len(paths)} paths.")
  for path in paths:
    if shortest == -1 or path < shortest:
      debug(f"Found path {path}, shortest {shortest}")
      shortest = path
  print(f"Returning {shortest}")
  return shortest

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
        debug(f"Visited {reindeer} already. BREAK")
        continue
      visited.append((reindeer[0], reindeer[1]))

    if maze[reindeer[1]][reindeer[0]] == 'E':
      print(f"Reached end! with {len(visited)} visits and score {score}. Visited: {visited}")
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
    

def printBots(botsOnGrid):
  print("---")
  for row in botsOnGrid:
    line = ""
    for x in range(len(row)):
      if row[x] == 0:
        line += ' '
      elif row[x] > 9:
        line += '#'
      else:
        line += str(row[x])
    print(line)
  print("---")


def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)
  startingPos, endPos = transform(input)

  #pathLength = shortestPath((startingPos[0], startingPos[1], '>'), endPos, False)
  pathLength = shortestPathViaList((startingPos[0], startingPos[1], '>'), endPos)

  print(f"Result for part 1: {str(pathLength)}")

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)
  startingPos = transform(input)

  pathLength = shortestPath((startingPos[0], startingPos[1], '>'), [], False)

  print(f"Result for part 2: {str(pathLength)}")

def solve():
  part1(True)
  #part2(True)