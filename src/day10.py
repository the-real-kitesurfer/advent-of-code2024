DAY = "10"

from helper import debug, fetchData

def computeScores(grid, startX, startY):
  nineHeights = []
  for move in [(1,0), (0,1), (-1,0), (0,-1)]:
      moveX = move[0]
      moveY = move[1]
      if(startX + moveX < 0) or (startY + moveY < 0) or (startX + moveX >= len(grid[0])) or (startY + moveY >= len(grid)):
        continue
      #debug("Checking " + str(grid[startY + moveY][startX + moveX]) + " at " + str(startX + moveX) + ", " + str(startY + moveY))
      if int(grid[startY + moveY][startX + moveX]) == int(grid[startY][startX]) + 1:
        if int(grid[startY + moveY][startX + moveX]) == 9:
          #debug("Found " + str(grid[startY + moveY][startX + moveX]) + " at " + str(startX + moveX) + ", " + str(startY + moveY))
          nineHeights.append((startX + moveX, startY + moveY))
        else:
          #debug("Continuing with " + str(grid[startY + moveY][startX + moveX]) + " at " + str(startX + moveX) + ", " + str(startY + moveY))
          for nineHeight in computeScores(grid, startX + moveX, startY + moveY):
            nineHeights.append(nineHeight)

  return nineHeights

def uniqueNineHeights(nineHeights):
  score = 0
  processed = []
  for nineHeight in nineHeights:
    if not nineHeight in processed:
      score += 1
      processed.append(nineHeight)
  return score

def processTrailheads(grid, uniqueCount):
  #uniqueNineHeights(computeScores(grid, 2, 5))
  if False:
    return [1]
  scores = []
  for y, row in enumerate(grid):
    for x, cell in enumerate(row):
      if cell == '0':
        nineHeights = uniqueNineHeights(computeScores(grid, x, y))
        if uniqueCount:
          thisScore = uniqueNineHeights(computeScores(grid, x, y))
        else:
          thisScore = len(computeScores(grid, x, y))

        debug("Processing " + str(cell) + " at " + str(x) + ", " + str(y) + ", score: " + str(thisScore))
        scores.append(thisScore)

  return scores

def sumOfScores(scores):
  result = 0
 
  for score in scores:
    result += score

  return result

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)

  print ("Transforming data")
  scores = processTrailheads(input, True)

  print("Result for part 1: " + str(sumOfScores(scores)))

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)

  print ("Transforming data")
  scores = processTrailheads(input, False)

  print("Result for part 2: " + str(sumOfScores(scores)))


def solve():
  part1(True)
  part2(True)


