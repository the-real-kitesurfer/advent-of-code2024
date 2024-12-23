DAY = "11"

from helper import DEBUG, debug, fetchData
from functools import lru_cache
from math import floor,log

def transform(input):
  stones = []
  for s in input[0].split(' '):
    stones.append(int(s))
  return stones

def blinkOld(stones):
  newStones = []
  for stone in stones:
    if stone == '0':
      newStones.append('1')
    elif len(stone) % 2 == 0:
      #debug("Splitting " + stone + " into " + str(int(stone[0:int(len(stone)/2)])) + " and " + str(int(stone[int(len(stone)/2):])))
      newStones.append(str(int(stone[0:int(len(stone)/2)])))
      newStones.append(str(int(stone[int(len(stone)/2):])))
    else:
      newStones.append(str(int(stone) * 2024))

  #if DEBUG: debug("New stones for input stones " + str(stones) + " are " + str(newStones))
  return newStones

@lru_cache(maxsize=None)
def blinkSingleStone(stone, timesToBlink):
  print("Blinks left: " + str(timesToBlink))
  newStones = []
  m=floor(log(stone,10))+1 if stone!=0 else 1
  if stone == 0:
    newStones.append(1)
  elif m % 2 == 0:
    #debug("Splitting " + stone + " into " + str(int(stone[0:int(len(stone)/2)])) + " and " + str(int(stone[int(len(stone)/2):])))
    newStones.append(stone//10**(m//2))
    newStones.append(stone%10**(m//2))
  else:
    newStones.append(stone * 2024)

  newStones3 = []
  for newStone in newStones:
    if timesToBlink > 0:
      newStones2 = blinkSingleStone(newStone, timesToBlink - 1)
    else:
      newStones2 = [newStone]
    for newStone2 in newStones2:
      newStones3.append(newStone2)

  #if DEBUG: debug("New stones for input stones " + str(stones) + " are " + str(newStones))
  return newStones3

def blink(stones, timesToBlink):
  newStones = []
  for stone in stones:
    for newStone in blinkSingleStone(stone, timesToBlink):
      newStones.append(newStone)
  return newStones

#memo = {}
@lru_cache(maxsize=None)
def blinkDynamic(stone, timesToBlink):
  if timesToBlink == 0:
    return [stone]
  newStones = []
  for newStone in blink([stone]):
    for innerStones in blinkDynamic(newStone, timesToBlink - 1):
      for innerStone in innerStones:
        newStones.append(innerStone)
  return newStones

#memo = {}
@lru_cache(maxsize=None)
def blinkDynamic2(stone, timesToBlink):
  if timesToBlink == 0:
    return [stone]
  newStones = []
  for newStone in blink([stone]):
    for innerStones in blinkDynamic(newStone, timesToBlink - 1):
      for innerStone in innerStones:
        newStones.append(innerStone)
  return newStones

def blinkEfficiently(stoneCount, stones, timesToBlink):
  print(str(timesToBlink) + " blinks left")
  newStoneCount = 0
  if timesToBlink > 0:
    for stone in stones:
      newStones = []
      if stone == '0':
        newStones.append('1')
      elif len(stone) % 2 == 0:
        #debug("Splitting " + stone + " into " + str(int(stone[0:int(len(stone)/2)])) + " and " + str(int(stone[int(len(stone)/2):])))
        newStones.append(str(int(stone[0:int(len(stone)/2)])))
        newStones.append(str(int(stone[int(len(stone)/2):])))
      else:
        newStones.append(str(int(stone) * 2024))
      if DEBUG: debug("New stones with " + str(timesToBlink) + " blinks left: " + str(newStones))
      newStoneCount += blinkEfficiently(stoneCount, newStones, timesToBlink - 1)

    return newStoneCount
  else:
    return stoneCount

def blinkEfficientlyTake2(stoneCount, stones, timesToBlink):
  print(str(timesToBlink) + " blinks left")
  newStoneCount = 0
  if timesToBlink > 0:
    for stone in stones:
      newStones = []
      if stone == '0':
        newStones.append('1')
      elif len(stone) % 2 == 0:
        #debug("Splitting " + stone + " into " + str(int(stone[0:int(len(stone)/2)])) + " and " + str(int(stone[int(len(stone)/2):])))
        newStones.append(str(int(stone[0:int(len(stone)/2)])))
        newStones.append(str(int(stone[int(len(stone)/2):])))
      else:
        newStones.append(str(int(stone) * 2024))
      #if DEBUG: debug("New stones with " + str(timesToBlink) + " blinks left: " + str(newStones))
      newStoneCount += blinkEfficiently(stoneCount, newStones, timesToBlink - 1)

    return newStoneCount
  else:
    return stoneCount

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)
  stones = transform(input)

  #for i in range(75):
  #print ("Blinking #" + str(i+1))
  stones = blink(stones, 74)

  print("Result for part 1: " + str(len((stones))))

# final (?) idea: store final count of stones for each starting stone; maintain expansion to all stonews where needed, but use count whenever possible
def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)
  initialStones = transform(input)

  stoneCount = 0
  lastPrintedCount = 1
  stonesPerBlinkCount = {}
  if useRealData:
    #stonesPerBlinkCount = {75:initialStones}
    stonesPerBlinkCount[75] = []
    for initialStone in initialStones:
      stonesPerBlinkCount[75].append((initialStone, 1))
  else:
    #stonesPerBlinkCount = {25: initialStones}
    stonesPerBlinkCount[25] = []
    for initialStone in initialStones:
      stonesPerBlinkCount[25].append((initialStone, 1))
 # new idea: put computations into list (as (stone,blinks); process entry and store new entry - (newStone_i, blinks -1); then process always the smallest blink number to keep the size of the queue small
  while len(stonesPerBlinkCount) > 0:
    # find smallest blink count
    # blink
    # update stonesPerCount
    # count number of new stones (i.e., newStones - oldStones)
    # print("len(stonesPerBlinkCount): " + str(len(stonesPerBlinkCount)))
    lowestBlinkCount = -1
    highestBlinkCount = -1
    for blinkCount in stonesPerBlinkCount.keys():
      if len(stonesPerBlinkCount[blinkCount]) > 0 and (blinkCount < lowestBlinkCount or lowestBlinkCount == -1):
        lowestBlinkCount = blinkCount
      if len(stonesPerBlinkCount[blinkCount]) > 0 and (blinkCount > highestBlinkCount):
        highestBlinkCount = blinkCount
    if lowestBlinkCount == -1:
      break
    
    if stoneCount > 10 * lastPrintedCount:
      lastPrintedCount = stoneCount
      if DEBUG: debug("Current stoneCount: " + str(stoneCount) + "; lbc: " + str(lowestBlinkCount) + ", hbc: " + str(highestBlinkCount))
    #if DEBUG: debug("Current stoneCount: " + str(stoneCount) + "; lbc: " + str(lowestBlinkCount) + ", hbc: " + str(highestBlinkCount) + ": spbc: " + str(stonesPerBlinkCount))
    stone,noOfSameStone = stonesPerBlinkCount[lowestBlinkCount].pop()

    stoneCount -= noOfSameStone
    newStones = blinkSingleStone(stone, 1)
    #newStones = blinkDynamic([stone], timesToBlink)
    stoneCount += noOfSameStone*len(newStones)
    #if len(newStones) > 1: debug("Split stone '" + str(stone) + "' into " + str(len(newStones)) + " stones, new stoneCount: " + str(stoneCount))
    if lowestBlinkCount > 1:
      if not (lowestBlinkCount - 1) in stonesPerBlinkCount:
        stonesPerBlinkCount[lowestBlinkCount - 1] = []
      for newStone in newStones:
        added = False
        for i, (existingStone, existingCount) in enumerate(stonesPerBlinkCount[lowestBlinkCount - 1]):
          if existingStone == newStone:
            stonesPerBlinkCount[lowestBlinkCount - 1].pop(i)
            stonesPerBlinkCount[lowestBlinkCount - 1].append((newStone, existingCount + noOfSameStone))
            added = True
            break
        if not added:
          stonesPerBlinkCount[lowestBlinkCount - 1].append((newStone, noOfSameStone))

  print("Result for part 2: " + str(stoneCount))


def solve():
  #part1(True)
  part2(False)


