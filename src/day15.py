DAY = "15"

from helper import DEBUG, debug, fetchData

def transform(input):
  warehouse = []
  movements = []
  botPosition = []
  for y,row in enumerate(input):
    if len(row) > 0:
      if row[0] == '#':
        line = []
        for x,c in enumerate(row):
          if c == '@':
            line.append('.')
            botPosition.append(x)
            botPosition.append(y)
          else:
            line.append(c)
        warehouse.append(line)
      else:
        for c in row:
          movements.append(c)

  return warehouse, movements, botPosition

def makeWide(warehouse):
  wideWarehouse = []
  for row in warehouse:
    wideRow = []
    for c in row:
      if c == 'O':
        wideRow.append('[')
        wideRow.append(']')
      else:
        wideRow.append(c)
        wideRow.append(c)
    wideWarehouse.append(wideRow)
  return wideWarehouse

def gps(x, y):
  return 100*y + x

def gpsWide(x, y, w, h):
  result = 0
  if y < h//2:
    #debug(f"y part: {100*y}")
    result = 100*y
  else:
    #debug(f"y part: {100*(h-y)}")
    result = 100*(h-y)
  if x < w//2:
    #debug(f"x part: {x}")
    return result + x
  else:
    #debug(f"x part: {w-x}")
    return result + w - x

def move(warehouse, movement, botPosition):
  isBox = False
  initialBox = None

  debug(f"Trying to move bot {movement} from {botPosition}")
  if movement == '<':
    y = botPosition[1]
    for x in range(botPosition[0]-1, 0, -1):
      #debug(f"Trying to move bot {movement} from {botPosition}, checking position {x}, {y}: {warehouse[y][x]}")
      if warehouse[y][x] == '#':
        break
      if warehouse[y][x] == 'O':
        if not initialBox:
          initialBox = (x,y)
      elif warehouse[y][x] == '.':
        if initialBox:
          debug(f"Moved box at {initialBox[0]}, {initialBox[1]} {movement}")
          warehouse[initialBox[1]][initialBox[0]] = '.'
          warehouse[y][x] = 'O'
        botPosition[0] -= 1
        debug(f"Moved box(es) {movement}, new botPosition: {botPosition}")
        return

  if movement == '>':
    y = botPosition[1]
    for x in range(botPosition[0]+1, len(warehouse[0]), +1):
      #debug(f"Trying to move bot {movement} from {botPosition}, checking position {x}, {y}: {warehouse[y][x]}")
      if warehouse[y][x] == '#':
        break
      if warehouse[y][x] == 'O':
        if not initialBox:
          initialBox = (x,y)
      elif warehouse[y][x] == '.':
        if initialBox:
          debug(f"Moved box at {initialBox[0]}, {initialBox[1]} {movement}")
          warehouse[initialBox[1]][initialBox[0]] = '.'
          warehouse[y][x] = 'O'
        botPosition[0] += 1
        debug(f"Moved box(es) {movement}, new botPosition: {botPosition}")
        return

  if movement == '^':
    x = botPosition[0]
    for y in range(botPosition[1]-1, 0, -1):
      #debug(f"Trying to move bot {movement} from {botPosition}, checking position {x}, {y}: {warehouse[y][x]}")
      if warehouse[y][x] == '#':
        break
      if warehouse[y][x] == 'O':
        if not initialBox:
          initialBox = (x,y)
      elif warehouse[y][x] == '.':
        if initialBox:
          debug(f"Moved box at {initialBox[0]}, {initialBox[1]} {movement}")
          warehouse[initialBox[1]][initialBox[0]] = '.'
          warehouse[y][x] = 'O'
        botPosition[1] -= 1
        debug(f"Moved box(es) {movement}, new botPosition: {botPosition}")
        return

  if movement == 'v':
    x = botPosition[0]
    for y in range(botPosition[1]+1, len(warehouse), +1):
      #debug(f"Trying to move bot {movement} from {botPosition}, checking position {x}, {y}: {warehouse[y][x]}")
      if warehouse[y][x] == '#':
        break
      if warehouse[y][x] == 'O':
        if not initialBox:
          initialBox = (x,y)
      elif warehouse[y][x] == '.':
        if initialBox:
          debug(f"Moved box at {initialBox[0]}, {initialBox[1]} {movement}")
          warehouse[initialBox[1]][initialBox[0]] = '.'
          warehouse[y][x] = 'O'
        botPosition[1] += 1
        debug(f"Moved box(es) {movement}, new botPosition: {botPosition}")
        return

def moveWide(warehouse, movement, botPosition):
  isBox = False
  movedBoxes = []

  debug(f"Trying to move bot {movement} from {botPosition}")
  if movement == '<':
    y = botPosition[1]
    dX = -1
    dY = 0
    for x in range(botPosition[0]-1, 0, -1):
      #debug(f"Trying to move bot {movement} from {botPosition}, checking position {x}, {y}: {warehouse[y][x]}")
      if warehouse[y][x] == '#':
        break
      if warehouse[y][x] == ']':
        movedBoxes.append((x,y))
      elif warehouse[y][x] == '[':
        movedBoxes.append((x,y))
      elif warehouse[y][x] == '.':
        for i in range(len(movedBoxes), 0, -1):
        #for movedBox in movedBoxes:
          movedBox = movedBoxes[i-1]
          warehouse[movedBox[1]+dY][movedBox[0]+dX] = warehouse[movedBox[1]][movedBox[0]]
          warehouse[movedBox[1]][movedBox[0]] = '.'

        botPosition[0] += dX
        botPosition[1] += dY
        warehouse[botPosition[1]][botPosition[0]] = '.'
        debug(f"Moved {len(movedBoxes)} box(es) {movement}, new botPosition: {botPosition}")
        return

  if movement == '>':
    y = botPosition[1]
    dX = +1
    dY = 0
    for x in range(botPosition[0]+1, len(warehouse[0]), +1):
      #debug(f"Trying to move bot {movement} from {botPosition}, checking position {x}, {y}: {warehouse[y][x]}")
      if warehouse[y][x] == '#':
        break
      if warehouse[y][x] == ']':
        movedBoxes.append((x,y))
      elif warehouse[y][x] == '[':
        movedBoxes.append((x,y))
      elif warehouse[y][x] == '.':
        for i in range(len(movedBoxes), 0, -1):
        #for movedBox in movedBoxes:
          movedBox = movedBoxes[i-1]
          warehouse[movedBox[1]+dY][movedBox[0]+dX] = warehouse[movedBox[1]][movedBox[0]]
          warehouse[movedBox[1]][movedBox[0]] = '.'

        botPosition[0] += dX
        botPosition[1] += dY
        warehouse[botPosition[1]][botPosition[0]] = '.'
        debug(f"Moved {len(movedBoxes)} box(es) {movement}, new botPosition: {botPosition}")
        return

  if movement == '^':
    dX = 0
    dY = -1
    for y in range(botPosition[1]-1, 0, -1):
      everythingFree = True
      wallFound = False
      for x in range(len(warehouse[0])):
        #debug(f"Trying to move bot {movement} from {botPosition}, checking position {x}, {y}: {warehouse[y][x]}")
        if not (x,y+1) in movedBoxes and not x == botPosition[0]:
          # nothing below moved -> skip
          continue
        if warehouse[y][x] == '#':
          everythingFree = False
          wallFound = True
          break
        if warehouse[y][x] == ']':
          everythingFree = False
          movedBoxes.append((x-1,y)) #also move box to the left
          movedBoxes.append((x,y))
        elif warehouse[y][x] == '[':
          everythingFree = False
          movedBoxes.append((x,y))
          movedBoxes.append((x+1,y)) #also move box to the right
        #elif warehouse[y][x] == '.':
        # nothing to do -> we found an empty space!
      
      if wallFound:
        break

      if everythingFree:
        for i in range(len(movedBoxes), 0, -1):
        #for movedBox in movedBoxes:
          movedBox = movedBoxes[i-1]
          warehouse[movedBox[1]+dY][movedBox[0]+dX] = warehouse[movedBox[1]][movedBox[0]]
          warehouse[movedBox[1]][movedBox[0]] = '.'

        botPosition[0] += dX
        botPosition[1] += dY
        warehouse[botPosition[1]][botPosition[0]] = '.'
        debug(f"Moved {len(movedBoxes)} box(es) {movement}, new botPosition: {botPosition}")
        return

  if movement == 'v':
    dX = 0
    dY = +1
    for y in range(botPosition[1]+1, len(warehouse), +1):
      everythingFree = True
      wallFound = False
      for x in range(len(warehouse[0])):
        #debug(f"Trying to move bot {movement} from {botPosition}, checking position {x}, {y}: {warehouse[y][x]}")
        if not (x,y-1) in movedBoxes and not x == botPosition[0]:
          # nothing below moved -> skip
          continue
        if warehouse[y][x] == '#':
          wallFound = True
          everythingFree = False
          break
        if warehouse[y][x] == ']':
          everythingFree = False
          movedBoxes.append((x-1,y)) #also move box to the left
          movedBoxes.append((x,y))
        elif warehouse[y][x] == '[':
          everythingFree = False
          movedBoxes.append((x,y))
          movedBoxes.append((x+1,y)) #also move box to the right
        #elif warehouse[y][x] == '.':
          # nothing to do -> we found an empty space!

      if wallFound:
        break

      if everythingFree:
        for i in range(len(movedBoxes), 0, -1):
        #for movedBox in movedBoxes:
          movedBox = movedBoxes[i-1]
          warehouse[movedBox[1]+dY][movedBox[0]+dX] = warehouse[movedBox[1]][movedBox[0]]
          warehouse[movedBox[1]][movedBox[0]] = '.'

        botPosition[0] += dX
        botPosition[1] += dY
        warehouse[botPosition[1]][botPosition[0]] = '.'
        debug(f"Moved {len(movedBoxes)} box(es) {movement}, new botPosition: {botPosition}")
        return


def processMovements(warehouse, movements, botPosition, wide):
  n = 0
  for movement in movements:
    print(f"{movement}")
    if wide:
      moveWide(warehouse, movement, botPosition)
      #n += 1
      #if n > 100:
      #  return
    else:
      move(warehouse, movement, botPosition)
    printWarehouse(warehouse, botPosition, True or DEBUG)


def sumOfBoxPositions(warehouse):
  result = 0
  for y, row in enumerate(warehouse):
    for x, c in enumerate(row):
      if c == 'O':
        result += gps(x,y)

  return result

def sumOfBoxPositionsWide(warehouse):
  sum = 0
  for y, row in enumerate(warehouse):
    for x, c in enumerate(row):
      if c == '[':
        result = gps(x,y)
        debug(f"Result for {(x,y)}: {result}")
        sum += result

  return sum

def printWarehouse(warehouse, bot, visible):
  if not visible:
    return
  for y,row in enumerate(warehouse):
    line = ""
    lastC = ''
    for x,c in enumerate(row):
      if bot[0] == x and bot[1] == y:
        line += '@'
      else:
        line += c
        if (c == '[' and lastC == '[') or (c == ']' and lastC == ']'):
          print("SOMETHING WENT WRONG")
          exit(-1)
        lastC = c
    print(line)
  print("")

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)

  warehouse, movements, botPosition = transform(input)

  processMovements(warehouse, movements, botPosition, False)

  result = sumOfBoxPositions(warehouse)

  print(f"Result for part 1: {str(result)}")

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)

  warehouse, movements, botPosition = transform(input)
  warehouse = makeWide(warehouse)
  botPosition[0] = 2 * botPosition[0]

  printWarehouse(warehouse, botPosition, True)

  processMovements(warehouse, movements, botPosition, True)

  printWarehouse(warehouse, botPosition, True)

  result = sumOfBoxPositionsWide(warehouse)

  print(f"Result for part 2: {str(result)} (should be 618 for the small example and 9021 for the big example ...)")

def solve():
  #part1(True)
  part2(False)