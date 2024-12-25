DAY = "25"

from helper import DEBUG, debug, fetchData
from functools import lru_cache

def transformLock(input, offset):
  debug(f"Transforming lock with offset {offset}, first row: {input[offset]}")
  lock = [0,0,0,0,0]
  for c in range(5):
    for h in range(7):
      if input[offset+h][c] == '#' and h > lock[c]:
        lock[c] = h

  return lock

def transformKey(input, offset):
  debug(f"Transforming key with offset {offset}, first row: {input[offset]}")
  key = [0,0,0,0,0]
  for c in range(5):
    for h in range(7):
      if input[offset+7-1-h][c] == '#' and h > key[c]:
        key[c] = h

  return key

def transform(input):
  locks = []
  keys = []
  i = 0
  while i < len(input):
    if len(input[i]) == 0:
      i += 1 #empty row
    elif input[i][0] == '#':
      locks.append(transformLock(input, i))
      i += 8
    elif input[i][0] == '.':
      keys.append(transformKey(input, i))
      i += 8
    else:
      print(f"Unexpected line found @ {i}: {input[i]}")

  debug(f"locks: {locks}")
  debug(f"keys: {keys}")

  return locks, keys

def findCombinations(locks, keys):
  combinations = []
  for lock in locks:
    for key in keys:
      allFit = True
      for c in range(5):
        if lock[c] + key[c] > 5:
          allFit = False
          break
      if allFit:
        debug(f"Lock {lock} fits to key {key}")
        combinations.append((lock,key))

  return combinations

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)
  locks, keys = transform(input)

  combinations = findCombinations(locks, keys)

  print(f"Result for part 1: {len(combinations)} ({len(locks)} locks and {len(keys)} keys)") #    my binary: 0b000000000000001101101110
  print(f"Expected:          3 (2 locks and 3 keys)") # correct binary:              0011111101000


def solve():
  part1(True)
  #part2(False)