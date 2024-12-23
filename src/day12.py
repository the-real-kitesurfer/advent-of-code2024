DAY = "12"

from helper import DEBUG, debug, fetchData

def transform(input):
  grid = []
  for row in input:
    grid.append(row)
  return grid

def growRegion(grid, x, y, region, used):
  if not (x,y) in used:
    region.append((x,y))
    used.append((x,y))

    for moveX, moveY in [(+1,0), (-1,0), (0,+1), (0,-1)]:
      if x + moveX >= 0 and x + moveX < len(grid[0]) and y + moveY >= 0 and y + moveY < len(grid) and grid[y][x] == grid[y+moveY][x+moveX]:
        region, used = growRegion(grid, x + moveX, y + moveY, region, used)

  return region, used

def findRegions(grid):
  regions = []
  usedPositions = []
  thisRegion = []
  for y, row in enumerate(grid):
    for x in range(len(row)):
      region, usedPositions = growRegion(grid, x, y, [], usedPositions)
      regions.append(region)

  return regions

def computeArea(region):
  return len(region)

def computePerimeter(grid, region):
  perimeter = 0
  for position in region:
    x = position[0]
    y = position[1]
    for moveX, moveY in [(+1,0), (-1,0), (0,+1), (0,-1)]:
      if (x + moveX < 0) or (x + moveX >= len(grid[0])) or (y + moveY < 0) or (y + moveY >= len(grid)) or (not grid[y][x] == grid[y+moveY][x+moveX]):
        perimeter += 1
  return perimeter

def computePrice(grid, regions):
  pricePerRegion = []
  for region in regions:
    if len(region) > 0:
      debug("Region for '" + str(grid[region[0][1]][region[0][0]]) + "' has area " + str(computeArea(region)) + " and perimeter " + str(computePerimeter(grid, region)))
      pricePerRegion.append(computeArea(region) * computePerimeter(grid, region))
  return pricePerRegion

def ensureFenchesDictIsReady(fences, key):
  if not key in fences:
    fences[key] = {}

def isFence(fences, x, y):
  if y in fences:
    if x in fences[y]:
      #debug(f"fences[y][x] = {fences[y][x]}")
      return fences[y][x] == 'F'
    #debug(f"{x} not in {fences[y]}")
    return False

  #debug(f"{y} not in {fences}")
  return False

def isPlant(x, y, region):
  return (x,y) in region

def computeSides(grid, region):
  # new idea: cnt every f once vertically and horizontally, if they have no left/top neightbouring fence
  fences={}
  fencePositions = []
  fences2={}
  #for n in range(len(grid) + 2):
  #  fences.append(emptyRow(len(grid[0]) +2))

  plant = '?'
 
  lastFencePos = (-10,-10)
  for position in region:
    x = position[0]
    y = position[1]
    plant = grid[y][x]

    for moveX, moveY in [(+1,0), (-1,0), (0,+1), (0,-1)]:
      if (x + moveX < 0) or (x + moveX >= len(grid[0])) or (y + moveY < 0) or (y + moveY >= len(grid)):
        ensureFenchesDictIsReady(fences, y + moveY)
        fences[y + moveY][x + moveX] = 'F'
        if (x + moveX, y + moveY) not in fencePositions:
          fencePositions.append((x + moveX, y + moveY))
        lastFencePos=(x + moveX,y + moveY)
      elif (not grid[y][x] == grid[y+moveY][x+moveX]):
        ensureFenchesDictIsReady(fences, y + moveY)
        fences[y + moveY][x + moveX] = 'F'
        if (x + moveX, y + moveY) not in fencePositions:
          fencePositions.append((x + moveX, y + moveY))
        lastFencePos=(x + moveX,y + moveY)

  # add fences at corners
  for x in range(0,len(grid[0])):
    for y in range(0,len(grid)):
      for moveX, moveY in [(+1,+1), (+1,-1), (-1,+1), (-1,-1)]:
        if isFence(fences, x, y) and isFence(fences, x+moveX, y+moveY):
          if y + moveY >= len(grid) or x >= len(grid[0]) or x< 0 or not grid[y+moveY][x] == plant:
            ensureFenchesDictIsReady(fences, y + moveY)
            #fences[y+moveY][x] = 'F'
          elif y >= len(grid) or x+moveX >= len(grid[0]) or y< 0 or not grid[y][x+moveX] == plant:
            ensureFenchesDictIsReady(fences, y)
            #fences[y][x+moveX] = 'F'

  if DEBUG:
    printWithFencesAndCorners(grid, fences, [])

  sideCnt = 0

  # 1. find TL corner of fence - 1 side
  # 2. move left/right until end reached
  # 3. move up/down - +1 side
  # 4. move up/down until end reached
  # 5. move left/right- +1 side
  # 6. continue with 2. until start reached

  visited = []

  for x in range(-1,len(grid[0])+1):
    for y in range(-1,len(grid)+1):
      # part 1a - check vertically, cnt each fence without neighbor ABOVE (and plant right)
      if isFence(fences, x, y) and not isFence(fences, x, y-1) and isPlant(x+1, y, region):
        sideCnt += 1
        debug(f"Found fence vertically: {(x,y)}")
      # part 1b - check vertically, cnt each fence without neighbor BELOW (and plant left)
      if isFence(fences, x, y) and not isFence(fences, x, y+1) and isPlant(x-1, y, region):
        sideCnt += 1
        debug(f"Found fence vertically: {(x,y)}")
      # part 2a - check horizontally, cnt each fence without neighbor LEFT (and plant below)
      if isFence(fences, x, y) and not isFence(fences, x-1, y) and isPlant(x, y+1, region):
        sideCnt += 1
        debug(f"Found fence horizontally: {(x,y)} - {isFence(fences, x, y)} and {isFence(fences, x-1, y)}")
      # part 2b - check horizontally, cnt each fence without neighbor RIGHT (and plant above)
      if isFence(fences, x, y) and not isFence(fences, x+1, y) and isPlant(x, y-1, region):
        sideCnt += 1
        debug(f"Found fence horizontally: {(x,y)} - {isFence(fences, x, y)} and {isFence(fences, x-1, y)}")

  return sideCnt
  

def computeCorners(grid, region):
  # idea: count corners -> == #sides
  fences={}
  fencePositions = []
  fences2={}
  #for n in range(len(grid) + 2):
  #  fences.append(emptyRow(len(grid[0]) +2))

  plant = '?'
 
  lastFencePos = (-10,-10)
  for position in region:
    x = position[0]
    y = position[1]
    plant = grid[y][x]

    for moveX, moveY in [(+1,0), (-1,0), (0,+1), (0,-1)]:
      if (x + moveX < 0) or (x + moveX >= len(grid[0])) or (y + moveY < 0) or (y + moveY >= len(grid)):
        ensureFenchesDictIsReady(fences, y + moveY)
        fences[y + moveY][x + moveX] = 'F'
        if (x + moveX, y + moveY) not in fencePositions:
          fencePositions.append((x + moveX, y + moveY))
        lastFencePos=(x + moveX,y + moveY)
      elif (not grid[y][x] == grid[y+moveY][x+moveX]):
        ensureFenchesDictIsReady(fences, y + moveY)
        fences[y + moveY][x + moveX] = 'F'
        if (x + moveX, y + moveY) not in fencePositions:
          fencePositions.append((x + moveX, y + moveY))
        lastFencePos=(x + moveX,y + moveY)

  corners = []
  # count corners
  for x in range(0,len(grid[0])):
    for y in range(0,len(grid)):
      for moveX, moveY in [(+1,+1), (+1,-1), (-1,+1), (-1,-1)]:
        if isPlant(x,y,region) and ((not isPlant(x+moveX, y+moveY,region) and isPlant(x+moveX, y,region) and isPlant(x, y+moveY,region)) or (isFence(fences, x + moveX, y) and isFence(fences, x, y + moveY))):
          debug(f"Found corner: {(x,y)} -> {(moveX,moveY)}")
          corners.append((x + moveX, y + moveY))

  if DEBUG:
    printWithFencesAndCorners(grid, fences, corners)

  return len(corners)
  

def computeBulkPrice(grid, regions):
  pricePerRegion = []
  for region in regions:
    if len(region) > 0:
      #if not str(grid[region[0][1]][region[0][0]]) == "F":
      #  continue #skip other regions for now
      area = computeArea(region)
      #sides = computeSides(grid, region)
      sides = computeCorners(grid, region)
      if sides < 4:
        print("!!!! ODD !!!! Region for '" + str(grid[region[0][1]][region[0][0]]) + "' has area " + str(area) + " and " + str(sides) + " sides")
        exit()
      else:
        print("Region for '" + str(grid[region[0][1]][region[0][0]]) + "' has area " + str(area) + " and " + str(sides) + " sides")
      pricePerRegion.append(area * sides)
  return pricePerRegion

def emptyRow(n):
  result = []
  for i in range(n):
    result.append(' ')
  return result

def printWithFencesAndCorners(grid, fences, corners):
  temp = []
  temp.append(emptyRow(len(grid[0]) + 2))
  for row in grid:
    temp.append(emptyRow(len(grid[0]) + 2))
  temp.append(emptyRow(len(grid[0]) + 2))

  for y, row in enumerate(grid):
    for x, p in enumerate(row):
      temp[y+1][x+1] = p

  for y in range(len(temp)):
    for x in range(len(temp[y])):
      if y-1 in fences and x-1 in fences[y-1]:
        temp[y][x] = fences[y-1][x-1].lower()
      if (x-1,y-1) in corners:
        temp[y][x] = '.'
     
  for row in temp:
    printMe = ""
    for c in row:
      printMe += c
    print(printMe)
  

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)
  grid = transform(input)

  regions = findRegions(grid)
  pricePerRegion = computePrice(grid, regions)
  totalPrice = 0
  for regionPrice in pricePerRegion:
    totalPrice += regionPrice

  print("Result for part 1: " + str(totalPrice))

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)
  grid = transform(input)

  regions = findRegions(grid)
  pricePerRegion = computeBulkPrice(grid, regions)
  totalPrice = 0
  for regionPrice in pricePerRegion:
    totalPrice += regionPrice

  print("Result for part 2: " + str(totalPrice))


def solve():
  #part1(True)
  part2(True)
