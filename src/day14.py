DAY = "14"

from helper import DEBUG, debug, fetchData
from functools import lru_cache

def transform(input):
  bots = []
  for row in input:
    posAndVel = row.split(" ")
    debug("Split " + row + " into " + str(posAndVel))
    if len(posAndVel) > 1:
      pos = posAndVel[0].split(',')
      vel = posAndVel[1].split(',')
      debug(f"Split pos into {str(pos)} and vel into {str(vel)}")
      bots.append((int(pos[0][2:]), int(pos[1]), int(vel[0][2:]), int(vel[1])))

  return bots

def move(bot, width, height):
  newX = bot[0] + bot[2]
  newY = bot[1] + bot[3]

  if newX < 0:
    newX = width + newX
  if newX >= width:
    newX = newX - width

  if newY < 0:
    newY = height + newY
  if newY >= height:
    newY = newY - height

  return (newX, newY, bot[2], bot[3])

def predict(bots, width, height, seconds):
  for i in range(seconds):
    movedBots = []
    for b, bot in enumerate(bots):
      movedBot = move(bot, width, height)
      if b == 0:
        debug(f"Bot #1's position: {str(movedBot)}")
      movedBots.append(movedBot)
    bots = movedBots
  return bots

def botsInArea(bots, x, y, width, height):
  cnt = 0
  for bot in bots:
    if bot[0] >= x and bot[0] < x+width and bot[1] >= y and bot[1] < y+height:
      cnt += 1
  return cnt

def computeSafetyFactor(bots, width, height):
  ul = botsInArea(bots, 0, 0, width // 2, height // 2)
  ur = botsInArea(bots, width // 2 + 1, 0, width // 2, height // 2)
  ll = botsInArea(bots, 0, height // 2 + 1, width // 2, height // 2)
  lr = botsInArea(bots, width // 2 + 1, height // 2 + 1, width // 2, height // 2)

  debug(f"{ul} * {ur} * {ll} * {lr} = { ul * ur * ll * lr}")
  return ul * ur * ll * lr

@lru_cache
def isInTree(bot, width, height):
  if bot[1] == height - 1:
    treeWidth = 1
  else:
    treeWidth = bot[1] + 1

  if bot[1] == height - 2:
    # anywhere on the 2nd last row
    return bot[0] > width // 2 - treeWidth and bot[0] < width // 2 + treeWidth
  else:
    # either on the left or right boundary
    return bot[0] == 1 + width // 2 - treeWidth or bot[0] == width // 2 + treeWidth - 1

def plotBots(bots, width, height):
  rows = []
  for y in range(height):
    row = []
    for x in range(width):
      row.append(0)
    rows.append(row)
  
  for bot in bots:
    rows[bot[1]][bot[0]] += 1

  return rows

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


def timeUntilEasterEgg(bots, width, height):
  # new goal: check if the bots covered area resembles a tree, i.e.
  # 'draw' all, find area with >= 80% of bots, and check shape
  seconds = 0
  lowestSafetyFactor = 999999999
  while True:
    seconds += 1
    bots = predict(bots, width, height, 1)
    safetyFactor = computeSafetyFactor(bots, width, height)
    debug(f"{seconds} seconds elapsed already ...")
    if safetyFactor < lowestSafetyFactor:
      botsOnGrid = plotBots(bots, width, height)
      printBots(botsOnGrid)
      lowestSafetyFactor = safetyFactor
      print(f"{seconds} seconds elapsed already ...")
    continue

    botsOnGrid = plotBots(bots, width, height)
    printBots(botsOnGrid)
    print(f"{seconds} seconds elapsed already ...")

    continue

    for treeTopY in range(height):
      for treeTopX in range(width):
        for treeHeight in range(height -1-2, height):
          debug(f"{treeTopX}, {treeTopY}, {treeHeight}")
          if treeTopY + treeHeight > height:
            break
          botsInTree = 0
          treeCovered = True
          for y, row in enumerate(botsOnGrid):
            for x in range(width):
              if isInTree((x-treeTopX, y-treeTopY), treeHeight - 1, treeHeight + 1):
                #if isInTree((x-treeTopX, y-treeTopY), 2 * treeHeight + 1, treeHeight):
                debug(f"Checking tree boundary at {x}, {y} for {treeTopX}, {treeTopY}, {treeHeight}")
                if row[x] == 0:
                  # no bot -> tree not covered, try next tree
                  treeCovered = False
                  debug(f"No bot at ({x}, {y})")
                  break
                debug(f"{row[x]} bots at ({x}, {y})")
                botsInTree += row[x]
          
          if treeCovered:
            print(f"{botsInTree} bots in tree-shape after {seconds} seconds for {treeTopX}, {treeTopY}, {treeHeight}!")
            if botsInTree > 0.8 * len(bots):
              print(f"Bots in tree-shape after {seconds} seconds!")
              printBots(botsOnGrid)
              return seconds

  return -1
    
def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)
  bots = transform(input)

  if useRealData:
    width, height = (101,103)
  else:
    width, height = (11,7)

  bots = predict(bots, width, height, 100)

  safetyFactor = computeSafetyFactor(bots, width, height)

  print(f"Result for part 1: {str(safetyFactor)}")

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)
  bots = transform(input)

  if useRealData:
    width, height = (101,103)
  else:
    width, height = (11,7)

  debug(f"(5,0) in tree: {str(isInTree((5,0,0,0), width, height))}")
  debug(f"(6,0) in tree: {str(isInTree((6,0,0,0), width, height))}")
  debug(f"(6,1) in tree: {str(isInTree((6,1,0,0), width, height))}")
  debug(f"(4,1) in tree: {str(isInTree((4,1,0,0), width, height))}")
  debug(f"(4,6) in tree: {str(isInTree((4,6,0,0), width, height))}")
  debug(f"(5,6) in tree: {str(isInTree((5,6,0,0), width, height))}")


  seconds = timeUntilEasterEgg(bots, width, height)

  safetyFactor = computeSafetyFactor(bots, width, height)

  print(f"Result for part 2: {str(safetyFactor)}")

def solve():
  #part1(True)
  part2(True)