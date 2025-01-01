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
    if timesToBlink > 1:
      newStones2 = blinkSingleStone(newStone, timesToBlink - 1)
    else:
      newStones2 = [newStone]
    for newStone2 in newStones2:
      newStones3.append(newStone2)

  #if DEBUG: debug("New stones for input stones " + str(stones) + " are " + str(newStones))
  return newStones3

@lru_cache(maxsize=None)
def blinkOnce(stone):
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

  return newStones

def blink(stones, timesToBlink):
  newStones = []
  for stone in stones:
    for newStone in blinkSingleStone(stone, timesToBlink):
      newStones.append(newStone)
  return newStones

def blinkGroupWise(stones, timesToBlink):  
  cntPerStone = {}
  for stone in stones:
    cntPerStone[stone] = 1

  for i in range(timesToBlink):
    print(f"Blink #{i}: cntPerStone = {cntPerStone}")
    print()
    # store groups from previous round in new list
    newCntPerStone = {}

    # blink once for each stone from the (stable) list
    for stone in cntPerStone:
      newStones = blinkOnce(stone)
      # add the new stones (weighted!)
      for newStone in newStones:
        if not newStone in newCntPerStone:
          newCntPerStone[newStone] = cntPerStone[stone]
        else:
          newCntPerStone[newStone] += cntPerStone[stone]

    # use the new counts per stone for the next round
    cntPerStone = newCntPerStone

  stoneCnt = 0
  for stone in cntPerStone:
    stoneCnt += cntPerStone[stone]

  return stoneCnt

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
  stones = blink(stones, 25)

  print("Result for part 1: " + str(len((stones))))

# final (?) idea: store final count of stones for each starting stone; maintain expansion to all stonews where needed, but use count whenever possible
def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)
  initialStones = transform(input)

  stoneCount = blinkGroupWise(initialStones, 75)

  print("Result for part 2: " + str(stoneCount))


def solve():
  #part1(True)
  part2(True)


