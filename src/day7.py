DAY = "7"

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

  print("Result for part 2: " + '?')

def solve():
  part1(False)
  #part2(True)