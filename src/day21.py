DAY = "21"

from helper import DEBUG, debug, fetchData
from functools import lru_cache
import itertools

def fromCoordinate(pos, isDoor):
  if isDoor:
    coordinates = {
      '7': (1,1),
      '8': (2,1),
      '9': (3,1),
      '4': (1,2),
      '5': (2,2),
      '6': (3,2),
      '1': (1,3),
      '2': (2,3),
      '3': (3,3),
      '0': (2,4),
      'A': (3,4)
    }
  else:
    coordinates = {
    '^': (2,1),
    'A': (3,1),
    '<': (1,2),
    'v': (2,2),
    '>': (3,2)
    }

  for key in coordinates:
    if coordinates[key] == pos:
      return key
  debug(f"Did not find key for {pos} (onDoor: {isDoor})")
  return "?"

def validate(typed, firstKeypad, inFocus):
  focusedPos = coordinate(inFocus, firstKeypad)
  for i, c in enumerate(typed):
    if c == '<': focusedPos = (focusedPos[0] - 1, focusedPos[1])
    if c == '>': focusedPos = (focusedPos[0] + 1, focusedPos[1])
    if c == '^': focusedPos = (focusedPos[0], focusedPos[1]-1)
    if c == 'v': focusedPos = (focusedPos[0], focusedPos[1]+1)
    keyInFocus = fromCoordinate(focusedPos, firstKeypad)
    if keyInFocus == '?':
      debug(f"Lost focus when typing character {i} ({c}) from {typed} with focus on {inFocus} on firstKeypad: {firstKeypad}")
      return False
  return True

@lru_cache(maxsize=None)
def coordinate(c, isDoor):
  if isDoor:
    coordinates = {
      '7': (1,1),
      '8': (2,1),
      '9': (3,1),
      '4': (1,2),
      '5': (2,2),
      '6': (3,2),
      '1': (1,3),
      '2': (2,3),
      '3': (3,3),
      '0': (2,4),
      'A': (3,4)
    }
  else:
    coordinates = {
    '^': (2,1),
    'A': (3,1),
    '<': (1,2),
    'v': (2,2),
    '>': (3,2)
    }

  return coordinates[c]

@lru_cache(maxsize=None)
def deltaToKeys(x,y, xFirst):
  keysForX = {
    -2: "<<",
    -1: "<",
    0: "",
    +1: ">",
    +2: ">>",
  }    
  keysForY = {
    -3: "^^^",
    -2: "^^",
    -1: "^",
    0: "",
    +1: "v",
    +2: "vv",
    +3: "vvv"
  }    
  return [keysForX[x] + keysForY[y] + 'A', keysForY[y] + keysForX[x] + 'A']

@lru_cache(maxsize=None)
def findRoutes(c1, c2, firstKeypad):
  options = []
  for defaultXFirst in [True, False]:
    xFirst = defaultXFirst
    if firstKeypad: #the 1x9 grid on the final door
      if defaultXFirst and c1 in ['0', 'A']:
        xFirst = False
      if not defaultXFirst and c1 in ['7', '4', '1']:
        xFirst = True
    else: # the <^v> grid on one of the robots
      if defaultXFirst and c1 in ['^', 'A']:
        xFirst = False
      if not defaultXFirst and c1 in ['<']:
        xFirst = True

    pos1, pos2 = coordinate(c1, firstKeypad), coordinate(c2, firstKeypad)
    #debug(f"{pos1} -> {pos2} = {deltaToKeys(pos2[0] - pos1[0], pos2[1] - pos1[1], xFirst)} with xFirst = {xFirst}")
    for option in deltaToKeys(pos2[0] - pos1[0], pos2[1] - pos1[1], xFirst):
      # check: use only VALID sequences here ...
      if validate(option, firstKeypad, c1):
        options.append(option)
  return options

def typeIn(code, keypad, doValidation, origInFocus, lastKeyPad):
  # idea: track caller context, and then make stats, which char on keypad 1 resulted in which best option(s) on keypads 2..n; same for the char on level 2 etc ...
  if keypad == 1:
    debug("")

  options = [""]
  inFocus = origInFocus # 'A'
  for c in code:
    routesForC = []
    for route in findRoutes(inFocus, c, keypad == 1):
      routesForC.append(route)
    inFocus = c

    newOptions = []
    if False:
      bestNewLength = -1
      for route in routesForC:
        if bestNewLength == -1 or len(route) < bestNewLength:
          bestNewLength = len(route)

    for prevOption in options:
      for route in routesForC:
        if (True or len(route) == bestNewLength) and not prevOption + route in newOptions:
          newOptions.append(prevOption + route)
          if len(newOptions) % 1000 == 0:
            print(f"Found option #{len(newOptions)}")

    options = newOptions
    #debug(f" Need to type in {toTypePerXFirst[defaultXFirst]} for {code} on {keypad}, length {len(toTypePerXFirst[defaultXFirst])} with defaultXFirst: {defaultXFirst}")


  debug(f" Need to type in any of {options} for {code} on isFirstKeypad: {isFirstKeypad}")
  if doValidation:
    for option in options:
      if not validate(option, keypad == 1, origInFocus):
        print(f"Invalid sequence detected in {option} with focus on {origInFocus} on {keypad}")
        return []

  if keypad == lastKeyPad:
    if doValidation:
      if code == "029A":
        debug(f"Expected to type <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A, length {len("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A")}")
      else:
        debug(f"Expected length: Code 1 = 68, Code 2 = 60, Code 3 = 68, Code 4 = 64, Code 5 = 64")
    return options # toType
  else:
    if code == "029A":
      if keypad == 2: debug(f"Expected to type v<<A>>^A<A>AvA<^AA>A<vAAA>^A, length {len("v<<A>>^A<A>AvA<^AA>A<vAAA>^A")}")
      if keypad == 1: debug(f"Expected to type <A^A>^^AvvvA, length {len("<A^A>^^AvvvA")}")
    combinedOptions = []
    for i, option in enumerate(options):
      print(f"Checking option {i} of {len(options)}")
      innerOptions = typeIn(option, keypad + 1, doValidation, 'A', lastKeyPad)
      if innerOptions == []:
        print(f"Invalid sequence found in {option}  with focus {'A'} on {keypad + 1}")
        return []
      for innerOption in innerOptions:
        if not innerOption in combinedOptions:
          combinedOptions.append(innerOption)
    return combinedOptions

def shortestOption(options):
  shortest = -1
  for i, option in enumerate(options):
    debug(f"Option {i} of {len(options)} with length {len(option)}: {option}")
    if shortest == -1 or len(option) < len(options[shortest]):
      shortest = i
  return options[shortest]

def complexity(code, toType):
  numericPart = ""
  for c in code:
    if c in ['0','1','2','3','4','5','6','7','8','9']:
      numericPart += c
  #debug(f"Numeric part in {code} is {numericPart}")
  return int(numericPart) * len(toType)

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  codes = fetchData(DAY, useRealData)

  totalComplexity = 0
  for code in codes:
    shortest = ""
    inFocus = 'A'
    for c in code:
      toType = typeIn(c, 1, True or not useRealData, inFocus, 2+1)
      inFocus = c
      shortest += shortestOption(toType)
    debug(f"Shortest option from {toType} is {shortest}")
    totalComplexity += complexity(code, shortest)

  print(f"Result for part 1: {str(totalComplexity)}")
  print(f"Expected:          126384")

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  codes = fetchData(DAY, useRealData)

  totalComplexity = 0
  for code in codes:
    inFocus = 'A'
    shortest = ""
    for c in code:
      toType = typeIn(c, 1, True or not useRealData, inFocus, 4+1)
      inFocus = c
      shortest += shortestOption(toType)
    debug(f"Shortest option from {toType} is {shortest}")
    totalComplexity += complexity(code, shortest)

  print(f"Result for part 2: {str(totalComplexity)}")

def solve():
  seq = "<^<A"
  seq = "v<A<AA>>^AvAA^<A>Av<<A>>^AvA^Av<<A>>^AAv<A>A^A<A>Av<A<A>>^AAA<Av>A^A"
  #print(f"Permutations for {seq}: {permuteSequence(seq,3)}")
  part1(True)
  # attempt 1: 165516
  # attempt 2: 166048
  # attempt 3: 164684
  # attempt 4: 161952
  # attempt 5: 157908
  #part2(False)
