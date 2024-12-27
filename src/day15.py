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
      elif c == '@': # not necessary, the warehouse gets '.' during transform() for the bot position!
        wideRow.append('@')
        wideRow.append('.')
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
  exitAtEnd = False
  isBox = False
  movedBoxes = []

  debug(f"Trying to move bot {movement} from {botPosition}")
  if movement == '<':
    y = botPosition[1]
    dX = -1
    dY = 0
    for x in range(botPosition[0]-1, 0-1, -1):
      #debug(f"Trying to move bot {movement} from {botPosition}, checking position {x}, {y}: {warehouse[y][x]}")
      if warehouse[y][x] == '#':
        break
      if warehouse[y][x] == ']':
        movedBoxes.append((x,y,']'))
      elif warehouse[y][x] == '[':
        movedBoxes.append((x,y,'['))
      elif warehouse[y][x] == '.':
        for i in range(len(movedBoxes), 0, -1):
        #for movedBox in movedBoxes:
          movedBox = movedBoxes[i-1]
          warehouse[movedBox[1]+dY][movedBox[0]+dX] = movedBox[2]
          warehouse[movedBox[1]][movedBox[0]] = '.'

        botPosition[0] += dX
        botPosition[1] += dY
        warehouse[botPosition[1]][botPosition[0]] = '.'
        debug(f"Moved {len(movedBoxes)} box(es) {movement}, new botPosition: {botPosition}")
        return True

  if movement == '>':
    y = botPosition[1]
    dX = +1
    dY = 0
    for x in range(botPosition[0]+1, len(warehouse[0])+1, +1):
      #debug(f"Trying to move bot {movement} from {botPosition}, checking position {x}, {y}: {warehouse[y][x]}")
      if warehouse[y][x] == '#':
        break
      if warehouse[y][x] == ']':
        movedBoxes.append((x,y,']'))
      elif warehouse[y][x] == '[':
        movedBoxes.append((x,y,'['))
      elif warehouse[y][x] == '.':
        for i in range(len(movedBoxes), 0, -1):
        #for movedBox in movedBoxes:
          movedBox = movedBoxes[i-1]
          warehouse[movedBox[1]+dY][movedBox[0]+dX] = movedBox[2]
          warehouse[movedBox[1]][movedBox[0]] = '.'

        botPosition[0] += dX
        botPosition[1] += dY
        warehouse[botPosition[1]][botPosition[0]] = '.'
        debug(f"Moved {len(movedBoxes)} box(es) {movement}, new botPosition: {botPosition}")
        return True

  if movement == '^':
    dX = 0
    dY = -1
    everythingFree = False
    wallFound = False
    canMoveRobot = False
    for y in range(botPosition[1]-1, -1, -1):
      everythingFree = True
      emptyRowFound = True
      for x in range(len(warehouse[0])):
        #debug(f"Trying to move bot {movement} from {botPosition}, checking position {x}, {y}: {warehouse[y][x]}")
        if not (x,y-dY,'[') in movedBoxes and not (x,y-dY,']') in movedBoxes and not x == botPosition[0]:
          # nothing below moved -> skip
          continue
        if warehouse[y][x] == '#':
          everythingFree = False
          wallFound = True
          emptyRowFound = False
          break
        if warehouse[y][x] == ']':
          everythingFree = False
          if not (x-1,y,'[') in movedBoxes:
            movedBoxes.append((x-1,y,'[')) #also move box to the left
          if not (x,y,']') in movedBoxes:
            movedBoxes.append((x,y,']'))
          emptyRowFound = False
        elif warehouse[y][x] == '[':
          everythingFree = False
          if not (x,y,'[') in movedBoxes:
            movedBoxes.append((x,y,'['))
          if not (x+1,y,']') in movedBoxes:
            movedBoxes.append((x+1,y,']')) #also move box to the right
          emptyRowFound = False
        #elif warehouse[y][x] == '.':
        # nothing to do -> we found an empty space!

      if emptyRowFound:      
        canMoveRobot = True
        break
      if wallFound:
        break

    #if everythingFree:
    if canMoveRobot:
      for i in range(len(movedBoxes), 0, -1):
      #for movedBox in movedBoxes:
        movedBox = movedBoxes[i-1]
        warehouse[movedBox[1]+dY][movedBox[0]+dX] = movedBox[2]
        warehouse[movedBox[1]][movedBox[0]] = '.'

      botPosition[0] += dX
      botPosition[1] += dY
      warehouse[botPosition[1]][botPosition[0]] = '.'
      debug(f"Moved {len(movedBoxes)} box(es) {movement}, new botPosition: {botPosition}")
      return True

  if movement == 'v':
    dX = 0
    dY = +1
    everythingFree = False
    wallFound = False
    canMoveRobot = False
    for y in range(botPosition[1]+1, len(warehouse), +1):
      everythingFree = True
      emptyRowFound = True
      debug(f"emptyRowFound: {emptyRowFound} for {y}")
      for x in range(len(warehouse[0])):
        #debug(f"Trying to move bot {movement} from {botPosition}, checking position {x}, {y}: {warehouse[y][x]}")
        if not (x,y-dY,'[') in movedBoxes and not (x,y-dY,']') in movedBoxes and not x == botPosition[0]:
          # nothing below moved -> skip
          debug(f"Skipping {(x,y)} - { (x,y-1)} not in {movedBoxes}")
          continue
        if warehouse[y][x] == '#':
          wallFound = True
          everythingFree = False
          emptyRowFound = False
          break
        if warehouse[y][x] == ']':
          everythingFree = False
          if not (x-1,y,'[') in movedBoxes:
            movedBoxes.append((x-1,y,'[')) #also move box to the left
          if not (x,y,']') in movedBoxes:
            movedBoxes.append((x,y,']'))
          emptyRowFound = False
        elif warehouse[y][x] == '[':
          everythingFree = False
          if not (x,y,'[') in movedBoxes:
            movedBoxes.append((x,y,'['))
          if not (x+1,y,']') in movedBoxes:
            movedBoxes.append((x+1,y,']')) #also move box to the right
          emptyRowFound = False
        #elif warehouse[y][x] == '.':
          # nothing to do -> we found an empty space!
    
      if emptyRowFound:      
        canMoveRobot = True
        break
      if wallFound:
        break

    #if everythingFree:
    if canMoveRobot:
      for i in range(len(movedBoxes), 0, -1):
      #for movedBox in movedBoxes:
        movedBox = movedBoxes[i-1]
        debug(f"Moving box {movedBox}")
        if len(movedBoxes) > 400:
          if not exitAtEnd:
            printWarehouse(warehouse, botPosition, True)
          exitAtEnd = True

        warehouse[movedBox[1]+dY][movedBox[0]+dX] = movedBox[2]
        warehouse[movedBox[1]][movedBox[0]] = '.'

      botPosition[0] += dX
      botPosition[1] += dY
      warehouse[botPosition[1]][botPosition[0]] = '.'
      debug(f"Moved {len(movedBoxes)} box(es) {movement}, new botPosition: {botPosition}")
      if exitAtEnd:
        printWarehouse(warehouse, botPosition, True)
        exit(-2)
      return True
  
  return False # nothing moved


def processMovements(warehouse, movements, botPosition, wide):
  n = 0
  noOps = 0
  for i, movement in enumerate(movements):
    debug(f"{movement} (Step {i})")
    #if i > 30: exit()
    if wide:
      if not moveWide(warehouse, movement, botPosition):
        noOps += 1
      n += 1
      #if n > 100:
      #  return
    else:
      move(warehouse, movement, botPosition)
    printWarehouse(warehouse, botPosition, DEBUG)
  print(f"noOps: {noOps} of {n} movements overall")


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
        #result = gpsWide(x,y,len(warehouse[0]),len(warehouse)) # checked, this does not work here
        debug(f"Result for {(x,y)}: {result}")
        sum += result

  return sum

def printWarehouse(warehouse, bot, visible):
  if not visible:
    return
  somethingWentWrong = False
  boxCount = 0
  wallCount = 0
  for y,row in enumerate(warehouse):
    line = ""
    lastC = ''
    for x,c in enumerate(row):
      if bot[0] == x and bot[1] == y:
        line += '@'
      else:
        line += c

        if c == ']':
          boxCount += 1
        if c == '#':
          wallCount += 1

        if (c == '[' and lastC == '[') or (c == ']' and lastC == ']'):
          print("SOMETHING WENT WRONG")
          somethingWentWrong = True

        lastC = c
    print(line)
  print("")
  print(f"Found {boxCount} boxes and {wallCount} walls")
  if somethingWentWrong:
    exit(-1)

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

  print(f"Result for part 2: {str(result)} (should be 618 for the small example and 9021 for the big example ... 1425075 is wrong!)")

def solve():
  #part1(True)
  part2(True) 
  #tried:  1425075
  #part 1: 1414416