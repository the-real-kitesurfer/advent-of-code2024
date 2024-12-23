DAY = "19"

from helper import DEBUG, debug, fetchData
from functools import lru_cache

towels = []

def transform(input):
  global towels
  towels = []
  patterns = []
  for line in input:
    if len(towels) and len(line):
      patterns.append(line)
    if len(line.split(", ")) > 1:
      towels = line.split(", ")
  
  return towels, patterns

@lru_cache(maxsize=None)
def countVariationsForPattern(pattern):
  global towels
  variations = []

  debug(f"Trying to solve {pattern}")
  for towel in towels:
    debug(f"Does {pattern} start with {towel}? {pattern.startswith(towel)}")
    if pattern.startswith(towel):
      remainder = pattern[len(towel):]
      debug(f"{pattern} starts with {towel} - continuing with '{remainder}'")
      if len(remainder) == 0:
        debug(f"TADA - {pattern} is just towel {towel}")
        variations.append(1)
      else:
        variations.append(countVariationsForPattern(remainder))

  count = 0
  for variation in variations:
    count += variation
  return count

def countVariationsForPatterns(patterns):
  variations = 0
  for i, pattern in enumerate(patterns):
    debug(f"Solving pattern {i} / {len(patterns)}. Found {variations} variations already ...")
    variations += countVariationsForPattern(pattern)

  return variations

@lru_cache(maxsize=None)
def solvePattern(pattern):
  global towels

  debug(f"Trying to solve {pattern}")
  for towel in towels:
    debug(f"Does {pattern} start with {towel}? {pattern.startswith(towel)}")
    if pattern.startswith(towel):
      remainder = pattern[len(towel):]
      debug(f"{pattern} starts with {towel} - continuing with '{remainder}'")
      if len(remainder) == 0:
        debug(f"TADA - {pattern} is just towel {towel}")
        return True
      else:
        if solvePattern(remainder):
          debug(f"TADA - solved {pattern} recursively")
          return True

  return False

def solvePatterns(towels, patterns):
  solved = 0
  for i, pattern in enumerate(patterns):
    debug(f"Solving pattern {i} / {len(patterns)}. Solved {solved} already ...")
    if solvePattern(pattern):
      print(f"Tada - solved {pattern}")
      solved += 1

  return solved

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)

  towels, patterns = transform(input)

  solvedPatterns = solvePatterns(towels, patterns)

  print(f"Result for part 1: {str(solvedPatterns)}")

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)

  towels, patterns = transform(input)

  variations = countVariationsForPatterns(patterns)

  print(f"Result for part 2: {str(variations)}")

def solve():
  #part1(True)
  part2(True)

