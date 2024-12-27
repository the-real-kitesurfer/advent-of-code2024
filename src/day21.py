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

def validate(typed, isFirstKeypad, inFocus):
  focusedPos = coordinate(inFocus, isFirstKeypad)
  for i, c in enumerate(typed):
    if c == '<': focusedPos = (focusedPos[0] - 1, focusedPos[1])
    if c == '>': focusedPos = (focusedPos[0] + 1, focusedPos[1])
    if c == '^': focusedPos = (focusedPos[0], focusedPos[1]-1)
    if c == 'v': focusedPos = (focusedPos[0], focusedPos[1]+1)
    keyInFocus = fromCoordinate(focusedPos, isFirstKeypad)
    if keyInFocus == '?':
      debug(f"Lost focus when typing character {i} ({c}) from {typed} with focus on {inFocus} on isFirstKeypad: {isFirstKeypad}")
      return keyInFocus
  return keyInFocus

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
  #return [keysForX[x] + keysForY[y] + 'A', keysForY[y] + keysForX[x] + 'A']
  if xFirst:
    return keysForX[x] + keysForY[y] + 'A'
  else:
    return keysForY[y] + keysForX[x] + 'A'

@lru_cache(maxsize=None)
def findRoutes(c1, c2, isFirstKeypad):
  pos1, pos2 = coordinate(c1, isFirstKeypad), coordinate(c2, isFirstKeypad)
  # try to find optimal order without options -> maybe by identifying blocks: best solution for each current,next pair across 3 or more levels!?
  if isFirstKeypad: #the 1x9 grid on the final door
    xFirst = pos1[0] > pos2[0]
    if c1 in ['0', 'A'] and c2 in ['7', '4', '1']: #make sure to avoid the void by FIRST going up and then left
      xFirst = False
    if c1 in ['7', '4', '1'] and c2 in ['0', 'A']: #make sure to avoid the void by FIRST going right and then down
      xFirst = True
  else: # the <^v> grid on one of the robots
    xFirst = pos1[0] < pos2[0]
    if c1 in ['^', 'A'] and c2 == '<': #make sure to avoid the void by FIRST going down and then left
      xFirst = False
    if c1 in ['<'] and c2 in ['^', 'A']: #make sure to avoid the void by FIRST going right and then up
      xFirst = True

  #debug(f"{pos1} -> {pos2} = {deltaToKeys(pos2[0] - pos1[0], pos2[1] - pos1[1], xFirst)} with xFirst = {xFirst}")
  return deltaToKeys(pos2[0] - pos1[0], pos2[1] - pos1[1], xFirst)

def findRoutesOLD(c1, c2, keypad):
  options = []
  for defaultXFirst in [True, False]:
    xFirst = defaultXFirst
    if keypad == 1: #the 1x9 grid on the final door
      if defaultXFirst and c1 in ['0', 'A']:
        xFirst = False
      if not defaultXFirst and c1 in ['7', '4', '1']:
        xFirst = True
    else: # the <^v> grid on one of the robots
      if defaultXFirst and c1 in ['^', 'A']:
        xFirst = False
      if not defaultXFirst and c1 in ['<']:
        xFirst = True

    pos1, pos2 = coordinate(c1, keypad == 1), coordinate(c2, keypad == 1)
    #debug(f"{pos1} -> {pos2} = {deltaToKeys(pos2[0] - pos1[0], pos2[1] - pos1[1], xFirst)} with xFirst = {xFirst}")
    for option in deltaToKeys(pos2[0] - pos1[0], pos2[1] - pos1[1], xFirst):
      # check: use only VALID sequences here ...
      if not validate(option, keypad, c1) == '?':
        options.append(option)
  return options

def typeIn(code, keypad, doValidation, origInFocus, directionalKeypads):
  debug(f"Typing {code} on {keypad} with length {len(code)}")
  if keypad == 1:
    debug("")

  toType = ""
  inFocus = origInFocus # 'A'
  for i, c in enumerate(code):
    if i % 10000000 == 0:
      print(f"Finding routes for {i}th of {len(code)} chars on keypad {keypad} ({(100*i)//len(code)}%)")
    toType += findRoutes(inFocus, c, keypad == 1)
    #for route in findRoutes(inFocus, c, keypad == 1):
    #  routesForC.append(route)
    inFocus = c


  if DEBUG: debug(f" Need to type in {toType} for {code} on {keypad}")
  if doValidation:
    if validate(toType, keypad == 1, origInFocus) == '?':
      print(f"Invalid sequence detected in {toType} with focus on {origInFocus} on {keypad}")
      return []

  if keypad == directionalKeypads:
    if doValidation:
      if code == "029A":
        debug(f"Expected to type <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A, length {len("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A")}")
      else:
        debug(f"Expected length: Code 1 = 68, Code 2 = 60, Code 3 = 68, Code 4 = 64, Code 5 = 64")
    return [toType] # toType
  else:
    if code == "029A":
      if keypad == 2: debug(f"Expected to type v<<A>>^A<A>AvA<^AA>A<vAAA>^A, length {len("v<<A>>^A<A>AvA<^AA>A<vAAA>^A")}")
      if keypad == 1: debug(f"Expected to type <A^A>^^AvvvA, length {len("<A^A>^^AvvvA")}")

    innerOptions = typeIn(toType, keypad + 1, doValidation, 'A', directionalKeypads)
    if innerOptions == []:
      print(f"Invalid sequence found in {toType}  with focus {'A'} on {keypad + 1}")
      return []
    return innerOptions

def shortestOption(options):
  shortest = -1
  for i, option in enumerate(options):
    debug(f"Option {i} of {len(options)} with length {len(option)}: {option}")
    if shortest == -1 or len(option) < len(options[shortest]):
      shortest = i
  return options[shortest]

def longestOption(options):
  longest = -1
  for i, option in enumerate(options):
    debug(f"Option {i} of {len(options)} with length {len(option)}: {option}")
    if longest == -1 or len(option) > len(options[longest]):
      longest = i
  return options[longest]

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
  directionalKeypads = 2+1
  for code in codes:
    inFocus = 'A'
    result = ""
    for c in code:
      toType = typeIn(c, 1, True or not useRealData, inFocus, directionalKeypads)
      inFocus = c
      shortest = shortestOption(toType)
      debug(f"Shortest option from {toType} is {shortest}")
      result += shortest
    totalComplexity += complexity(code, result)

  print(f"Result for part 1: {str(totalComplexity)}")
  print(f"Expected:          126384")

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  codes = fetchData(DAY, useRealData)

  totalComplexity = 0
  directionalKeypads = 25+1
  for code in codes:
    inFocus = 'A'
    result = ""
    #code = "<vA<AA>>^AAvA<^A>AvA^A"
    for c in code:
      toType = typeIn(c, 1, False or not useRealData, inFocus, directionalKeypads)
      inFocus = c
      shortest = shortestOption(toType)
      shortestResult1 = reverse(shortest, 4, "A")
      shortestResult2 = reverse(shortestResult1, 3, "A")
      shortestResult3 = ""#reverse(shortestResult2, 2, "A")
      longest = longestOption(toType)
      longestResult1 = reverse(longest, 4, "A")
      longestResult2 = reverse(longestResult1, 3, "A")
      longestResult3 = ""#reverse(longestResult2, 2, inFocus)
      debug(f"Shortest option from {toType} is {shortest}")
      if len(shortest) < len(longest):
        print(f"for {c}: {len(shortest)} < {len(longest)}: {shortest} vs {longest} -> {shortestResult1} vs {longestResult1} -> {shortestResult2} vs {longestResult2} -> {shortestResult3} vs {longestResult3}")
      result += shortest
    totalComplexity += complexity(code, result)

  print(f"Result for part 2: {str(totalComplexity)}")

def reverse(option, keypad, inFocus):
  result = ""
  typed = ""
  for c in option:
    if c == 'A':
      result += typed
    else:
      typed = validate(c, keypad == 1, inFocus)
      #print(f"Typing {c} from {option} with focus on {inFocus} -> {typed}")
      inFocus = typed
  return result

def solve():
  # new approach - simple count groups, and their length on the next level
  seq = "<^<A"
  seq = "v<A<AA>>^AvAA^<A>Av<<A>>^AvA^Av<<A>>^AAv<A>A^A<A>Av<A<A>>^AAA<Av>A^A"
  #print(f"Permutations for {seq}: {permuteSequence(seq,3)}")
  part1(False)
  part1(True)
  # attempt 1: 165516
  # attempt 2: 166048
  # attempt 3: 164684
  # attempt 4: 161952
  # attempt 5: 157908

  #typeIn("3", 1, False, 'A')
  #typeIn("7", 1, False, '3')
  #typeIn("9", 1, False, '7')
  #typeIn("A", 1, False, '9')
  #print(typeIn("<", 3, True, 'A'))
  #+shortestOption(typeIn("2", 1, True, '0'))+shortestOption(typeIn("9", 1, True, '2'))+shortestOption(typeIn("A", 1, True, '9')))
  part2(True)
  return
  toType = typeIn("4", 1, True or not useRealData, "3", 4)
  shortest = shortestOption(toType)
  longest = longestOption(toType)
  debug(f"Shortest option from {toType} is {shortest} and longest is {longest}")
  for option in toType:
    result = reverse(option, 4, "A")
    result2 = reverse(result, 3, "A")
    result3 = reverse(result2, 2, "A")
    result4 = reverse(result3, 1, "3")
    print(f"{option} -> {result} -> {result2} -> {result3} ({len(option)} vs {len(result)} vs {len(result2)} vs {len(result3)})")

  # likely best to start from scratch :-o
  # 