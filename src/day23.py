DAY = "23"

from helper import DEBUG, debug, fetchData
from functools import lru_cache
import itertools

def addPair(pairs, left, right):
  if not left in pairs:
    pairs[left] = []
  pairs[left].append(right)
  if not right in pairs:
    pairs[right] = []
  pairs[right].append(left)
  
def transform(input):
  pairs = {}
  for line in input:
    addPair(pairs, line.split('-')[0], line.split('-')[1])

  debug(f"Turned {len(input)} lines into {len(pairs)} pairs")
  return pairs

def findsubsets(s, n):
  return list(itertools.combinations(s, n))

def sortedSet(n1, n2, n3):
  set = [n1,n2,n3]
  set.sort()
  return (set[0], set[1], set[2])

def findSets1(pairs):
  possibleSantaNodes = []
  for node in pairs.keys():
    if node[0] == 't' and not node in possibleSantaNodes:
      possibleSantaNodes.append(node)

  debug(f"{len(possibleSantaNodes)} nodes amongst all {len(pairs)} may belong to Santa")

  sets = []
  for node in possibleSantaNodes:
    combinations = findsubsets(pairs[node], 2)
    for combination in combinations:
      if combination[1] in pairs[combination[0]]:
        sorted = sortedSet(node, combination[0], combination[1])
        if sorted not in sets:
          sets.append(sorted)

  debug(f"Found {len(sets)} sets involving nodes that may belong to Santa")
  for set in sets:
    debug(set)

  return sets

def findSets2(pairs):
  nsets = {}
  nsets[2] = pairs

  n = 2
  while n in nsets:
    if n > 2:
      break
    n = n + 1
    for node in nsets[n-1].keys():
      combinations = findsubsets(nsets[n-1][node], n-1)
      for combination in combinations:
        allConnected = True
        for i in range(n-1):
          for j in range(n-1):
            if i == j:
              continue
            if not combination[i] in nsets[n-1][combination[j]]:
              allConnected = False
              break

          if not allConnected:
            break
        if allConnected:
          debug(f"-> {combination} found in {nsets[n-1]}")
          if not n in nsets:
            nsets[n] = {}
          if not node in nsets[n]:
            nsets[n][node] = []
          nsets[n][node].append(combination)
          #for node in nsets[n-1]:
          #  debug(f"{node}: {nsets[n-1][node]}")

  debug(f"Found {len(nsets[n-1])} biggest set")

  # sorted = sortedSet(node, combination[0], combination[1])
  # if sorted not in nsets[n]:

  for node in nsets[n-1]:
    debug(f"{node}: {nsets[n-1][node]}")

  return nsets[n-1]


def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)

  pairs = transform(input)
  sets = findSets1(pairs)

  print(f"Result for part 1: {len(sets)}")
  print(f"Expected:          {7}")

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)

  pairs = transform(input)
  sets = findSets2(pairs)

  print(f"Result for part 2: {len(sets)}")
  print(f"Expected:          {['co', 'de', 'ka', 'ta']}")

def solve():
  #part1(True)
  part2(False)