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
  nsets[2] = []
  for pairLeft in pairs:
    for pairRight in pairs[pairLeft]:
      nsets[2].append([pairLeft, pairRight])

  # continue here, idea: pick entry from n-1 set, exchange first entry with one entry from the pairs, and check that it is an set as well
  # seems to work, but very slow; idea: do not add entries from pairs but rather from m-set (and use the biggest m < n possible)
  n = 2
  while n in nsets:
    n = n + 1
    print(f"n={n} with {len(nsets[n-1])} entries")
    if n > 30:
      break
    for nset in nsets[n-1]:
      exchanged = nset[0]
      for linked in pairs[exchanged]:
        debug(f"Checking if {nset} with {exchanged} replaced by {linked} is a {n-1}-set as well")
        sorted = []
        for node in nset:
          if not node == exchanged:
            sorted.append(node)
        if not linked in sorted:
          sorted.append(linked)
          sorted.sort()
          if sorted in nsets[n-1]:
            sorted.append(exchanged)
            sorted.sort()
            if not n in nsets:
              nsets[n] = []
            if not sorted in nsets[n]:
              nsets[n].append(sorted)
              if len(nsets[n]) % 10000 == 0
                print(f"Already {len(nsets[n])} entries for n={n}")

  debug(f"Found {len(nsets[n-1])} biggest set for n={n-1}")

  for node in nsets[n-1]:
    debug(f"{node}")

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

  print(f"Result for part 2: {len(sets)} -> {sets}")
  print(f"Expected:          1 -> {['co', 'de', 'ka', 'ta']}")

def solve():
  #part1(True)
  part2(True)