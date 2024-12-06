DAY = "6"

from helper import debug

def fetchData(file):
  with open("./resources/" + file, 'r') as f:
    lines = f.readlines()
    listOfStrings=[]
    for i, line in enumerate(lines):
      listOfStrings.append(line[:-1])
  
  return listOfStrings

def transform(input):
  grid = []
  positionOfGuard = (-1,-1,'?') #x,y, direction <^>v
  for l, line in enumerate(input):
    for c, char in enumerate(line):
      if char in "<^>v":
        positionOfGuard = (c, l, char)
    grid.append(line)

  debug("positionOfGuard is " + str(positionOfGuard))
  return grid, positionOfGuard

def isObstacle(grid, positionOfGuard, moveX, moveY):
  return positionOfGuard[1] + moveY >= 0 and positionOfGuard[0] + moveX >= 0 and positionOfGuard[1] + moveY < len(grid) and positionOfGuard[0] + moveX < len(grid[0]) and grid[positionOfGuard[1] + moveY][positionOfGuard[0] + moveX] == '#'

def advance(positionOfGuard):
  if positionOfGuard[2] == '<':
    positionOfGuard = (positionOfGuard[0] - 1, positionOfGuard[1], positionOfGuard[2])
  if positionOfGuard[2] == '^':
    positionOfGuard = (positionOfGuard[0], positionOfGuard[1] - 1, positionOfGuard[2])
  if positionOfGuard[2] == '>':
    positionOfGuard = (positionOfGuard[0] + 1, positionOfGuard[1], positionOfGuard[2])
  if positionOfGuard[2] == 'v':
    positionOfGuard = (positionOfGuard[0], positionOfGuard[1] + 1, positionOfGuard[2])
  return positionOfGuard

def turn(positionOfGuard):
  if positionOfGuard[2] == '<':
    positionOfGuard = (positionOfGuard[0], positionOfGuard[1], '^')
  elif positionOfGuard[2] == '^':
    positionOfGuard = (positionOfGuard[0], positionOfGuard[1] , '>')
  elif positionOfGuard[2] == '>':
    positionOfGuard = (positionOfGuard[0], positionOfGuard[1], 'v')
  elif positionOfGuard[2] == 'v':
    positionOfGuard = (positionOfGuard[0], positionOfGuard[1], '<')
  return positionOfGuard

def moveGuard(grid, positionOfGuard):
  turned = False
  if positionOfGuard[2] == '<': 
    if isObstacle(grid, positionOfGuard, -1, 0):
      positionOfGuard = turn(positionOfGuard)
      turned = True
  elif positionOfGuard[2] == '^':
    if isObstacle(grid, positionOfGuard, 0, -1):
      positionOfGuard = turn(positionOfGuard)
      turned = True
  elif positionOfGuard[2] == '>': 
    if isObstacle(grid, positionOfGuard, +1, 0):
      positionOfGuard = turn(positionOfGuard)
      turned = True
  elif positionOfGuard[2] == 'v':
    if isObstacle(grid, positionOfGuard, 0, +1):
      positionOfGuard = turn(positionOfGuard)
      turned = True

  if not turned:
    positionOfGuard = advance(positionOfGuard)

  return positionOfGuard

def observeGuard(grid, positionOfGuard):
  visited = []
  for row in grid:
    emptyRow = []
    for x in range(len(row)):
      emptyRow.append(0)
    visited.append(emptyRow)

  while True:
    visited[positionOfGuard[1]][positionOfGuard[0]] = 1
    positionOfGuard = moveGuard(grid, positionOfGuard)

    debug("Position of guard: " + str(positionOfGuard))
    for row in visited:
      debug(row)
    debug("----")

    if positionOfGuard[0] < 0 or positionOfGuard[1] < 0 or positionOfGuard[1] >= len(grid) or positionOfGuard[0] >= len(grid[0]):
      return visited

def countVisitedPositions(visited):
  uniquePositions = 0
  for row in visited:
    for cell in row:
      uniquePositions += cell

  return uniquePositions

def checkIfTrapped(grid, positionOfGuard):
  visited = []
  for row in grid:
    emptyRow = []
    for x in range(len(row)):
      emptyRow.append("")
    visited.append(emptyRow)

  while True:
    if positionOfGuard[2] in visited[positionOfGuard[1]][positionOfGuard[0]]:
      return True
    visited[positionOfGuard[1]][positionOfGuard[0]] += positionOfGuard[2]
    positionOfGuard = moveGuard(grid, positionOfGuard)

    debug("Position of guard: " + str(positionOfGuard))
    for row in visited:
      debug(row)
    debug("----")

    if positionOfGuard[0] < 0 or positionOfGuard[1] < 0 or positionOfGuard[1] >= len(grid) or positionOfGuard[0] >= len(grid[0]):
      return False

def createTraps(grid, positionOfGuard):
  tries = 0
  numberOfTraps = 0
  modifiedGrid = []
  for x in range(len(grid[0])):
    for y in range(len(grid)):
      modifiedGrid = []
      for r, row in enumerate(grid):
        modifiedRow = []
        for c, char in enumerate(row):
          if x == c and y == r:
            modifiedRow.append('#')
          else:
            modifiedRow.append(char)
        modifiedGrid.append(modifiedRow)

      debug("Check if guard is trapped")
      tries += 1
      if tries % 1000 == 0:
        print(str(tries) + ". attempt to trap the guard ...")

      if checkIfTrapped(modifiedGrid, positionOfGuard):
        debug("Guard is trapped!")
        numberOfTraps += 1
        if numberOfTraps % 100 == 0:
          print("Guard trapped already " + str(numberOfTraps) + " times.")
  return numberOfTraps

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  if useRealData:
    input = fetchData('day' + DAY + '.txt')
  else:
    input = fetchData('sample' + DAY + '.txt')

  print ("Transforming data")
  grid, positionOfGuard = transform(input)

  print("Observing guard")
  visited = observeGuard(grid, positionOfGuard)

  print("Result for part 1: " + str(countVisitedPositions(visited)))

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  if useRealData:
    input = fetchData('day' + DAY + '.txt')
  else:
    input = fetchData('sample' + DAY + '.txt')

  print ("Transforming data")
  grid, positionOfGuard = transform(input)

  print("Result for part 2: " + str(createTraps(grid, positionOfGuard)))

def solve():
  part1(False)
  #part2(True)