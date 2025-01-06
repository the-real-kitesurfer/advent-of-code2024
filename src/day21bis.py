DAY = "21"

from helper import DEBUG, debug, fetchData
from functools import lru_cache
import itertools

def permuteSingle(action):
  debug(f"permuteSingle for {action}")

  permutations = []
  for p in itertools.permutations(action):
    #debug(f"Processing {p}")
    toType = ""
    for c in p:
      toType += c[0]
    
    if not toType + 'A' in permutations:
      permutations.append(toType + 'A')

  debug(f"Created {len(permutations)} permutations for {action}: {permutations}")

  return permutations

@lru_cache(maxsize=None)
def countNumberClicks(toType, keypad):
  debug(f"countNumberClicks for {toType} on {keypad}")
  if keypad > 4:
    return len(toType)
  else:
    toTypeOnKeypad = ""
    inFocus = 'A'
    for c in toType:
      toTypeOnKeypad += tpyeIn(c, inFocus, keypad)
      inFocus = c
    return countNumberClicks(toTypeOnKeypad, keypad + 1)

def permuteSequence(sequence, keypad):
  print(f"permuteSequence for {sequence} on {keypad}")
  actions = []
  part = []
  for c in sequence:
    if c == 'A':
      actions.append(part)
      part = []
    else:
      part.append(c)

  print(f"Found {len(actions)} parts in {sequence}: {actions}")

  permutationsForSequence = []
  for i, action in enumerate(actions):
    permutationsForAction = permuteSingle(action)
    debug(f"Found {len(permutationsForAction)} permutations for {i}th action, {action}")

    # idea: keep only the most promising ones (= smallest number of clicks on HIGHER keypad)
    mostPromisingPermutations = []
    for perm in permutationsForAction:
      if not isSequenceValid('A', perm, keypad):
        continue
      numberClicks = countNumberClicks(perm, keypad + 1)
      debug(f"{numberClicks} needed for {perm}")
      if len(mostPromisingPermutations) == 0 or numberClicks < countNumberClicks(mostPromisingPermutations[0], keypad + 1):
        mostPromisingPermutations = [perm]
      elif numberClicks == countNumberClicks(mostPromisingPermutations[0], keypad + 1):
        mostPromisingPermutations.append(perm)

    print(f"Kept {mostPromisingPermutations} permutation as the best for {i}th action, {action}, on {keypad}")

    if len(permutationsForSequence) == 0:
      permutationsForSequence = [mostPromisingPermutations[0]]
    else:
      newPermutationsForSequence = []
      for permForSequence in permutationsForSequence:
        permForAction = mostPromisingPermutations[0]
        #for permForAction in permutationsForAction:
        newPermutationsForSequence.append(permForSequence + permForAction)
      permutationsForSequence = newPermutationsForSequence

  debug(f"Created {len(permutationsForSequence)} permutations for list with {len(actions)} actions - {permutationsForSequence} from {sequence} resp. {actions} as a list; first permutation: {permutationsForSequence[0][0]}")

  return permutationsForSequence


def isSequenceValid(inFocus, sequence, keypad):
  # inFocus = 'A'
  for c in sequence:
    debug(f"Validating {c} in sequence {sequence} on keypad {keypad}")
    if c == 'A':
      continue

    inFocus = changeFocus(inFocus, c, keypad)
    if not inFocus:
      return False
  return True

def changeFocus(inFocus, typed, keypad):
  debug(f"Changing focus from {inFocus} after pressing {typed} on keypad {keypad}")
  #1: robot on door, #2: robot on robot 1, #3: robot on robot 2, #4: I
  if keypad == 1:
    if typed == '<':
      if inFocus == 'A':
        return '0'
      else:
        if int(inFocus) < 1:
          return None
        else:
          debug(f"RETURNING_A {str(int(inFocus)-1)[0]}")
          return str(int(inFocus)-1)[0]
    if typed == '>':
      if inFocus == '0':
        return 'A'
      elif inFocus == 'A':
        return None # not allowed!
      else:
        debug(f"RETURNING_B {str(int(inFocus)+1)[0]}")
        return str(int(inFocus)+1)[0]
    if typed == '^':
      if inFocus == 'A':
        return '3'
      elif inFocus == '0':
        return '2'
      else:
        debug(f"RETURNING_C {str(int(inFocus)+3)[0]}")
        return str(int(inFocus)+3)[0]
    if typed == 'v':
      if inFocus == '3':
        return 'A'
      elif inFocus == '2':
        return '0'
      elif inFocus == 'A':
        return None # not allowed!
      else:
        if int(inFocus) < 3:
          return None
        else:
          debug(f"RETURNING_D {str(int(inFocus)-3)[0]}")
          return str(int(inFocus)-3)[0]

  # keypad 2..4:
  else:
    if inFocus == '<' and typed == '>':
      return 'v'
    elif inFocus == '>' and typed == '<':
      return 'v'
    elif inFocus == '>' and typed == '^':
      return 'A'
    elif inFocus == 'v' and typed == '<':
      return '<'
    elif inFocus == 'v' and typed == '>':
      return '>'
    elif inFocus == 'v' and typed == '^':
      return '^'
    elif inFocus == '^' and typed == '>':
      return 'A'
    elif inFocus == '^' and typed == 'v':
      return 'v'
    elif inFocus == 'A' and typed == '<':
      return '^'
    elif inFocus == 'A' and typed == 'v':
      return '>'
  debug(f"Oops ... can't change focus on keypad {keypad} from {inFocus} when typing {typed}")
  return None

def reposition(c, inFocus, keypad):
  debug(f"repositioning focus {inFocus} for {c} on {keypad}")
  #1: robot on door, #2: robot on robot 1, #3: robot on robot 2, #4: I
  if keypad == 1:
    if c in ['7', '8', '9']:
      if not inFocus in ['7', '8', '9']:
        toType = '^'
      #focus in right row
      elif c == '9':
        toType = '>'
      elif inFocus == '7':
        toType = '>'
      else:
        toType = '<'

    elif c in ['4', '5', '6']:
      if not inFocus in ['4', '5', '6']:
        if inFocus in ['7', '8', '9']:
          toType = 'v'
        else:
          toType = '^'
      #focus in right row
      elif c == '6':
        toType = '>'
      elif inFocus == '4':
        toType = '>'
      else:
        toType = '<'

    elif c in ['1', '2', '3']:
      if not inFocus in ['1', '2', '3']:
        if inFocus in ['4', '5', '6']:
          toType = 'v'
        else:
          toType = '^'
      #focus in right row
      elif c == '3':
        toType = '>'
      elif inFocus == '1':
        toType = '>'
      else:
        toType = '<'

    elif c in ['0', 'A']:
      if not inFocus in ['1', '0', 'A']:
        toType = 'v'
      elif inFocus == '1':
        toType = '>'
      elif c == '0' and inFocus == 'A':
        toType = '<'
      elif c == 'A' and inFocus == '0':
        toType = '>'

  # keypad 2..4
  else:
    if c == 'A':
      if inFocus in ['v', '>']:
        toType = '^'
      else:
        toType = '>'

    if c == '^':
      if inFocus in ['v', '>']:
        toType = '^'
      elif inFocus == '<':
        toType = '>'
      else:
        toType = '<'

    if c == 'v':
      if inFocus in ['^', 'A']:
        toType = 'v'
      elif inFocus == '<':
        toType = '>'
      else:
        toType = '<'

    if c == '<':
      if inFocus in ['^', 'A']:
        toType = 'v'
      else:
        toType = '<'

    if c == '>':
      if inFocus in ['<', 'v']:
        toType = '>'
      else:
        toType = 'v'

  debug(f"Typed {toType} for {c} with focus {inFocus}")
  oldFocus = inFocus
  inFocus = changeFocus(inFocus, toType, keypad)
  #if not inFocus:
    #print(f"Lost focus on keypad {keypad} for {toType} with old focus {oldFocus}")
    #exit()
  debug(f"New focus: {inFocus}")
  return toType, inFocus


def tpyeIn(c, inFocus, keypad):
  tries = 0
  toType = ""
  while not c == inFocus:
    prevFocus = inFocus
    typeHere, inFocus = reposition(c, inFocus, keypad)
    debug(f"Typed {typeHere} for {c}, new focus {inFocus}")
    if not inFocus:
      print(f"Oops, lost focus for {c} with focus {prevFocus} on {keypad}")
      exit()
    toType += typeHere
    tries += 1
    if tries % 1000 == 0:
      print(f"Stuck (?) with {tries} tries on c={c} with focus {inFocus} on {keypad}")
  
  debug("ACTIVATE")
  toType += 'A'
  
  return toType

def typeCode(codesToType, keypad):
  print(f"Called typeCode for {codesToType}, {keypad}")
  codes = []
  if keypad > 1:
    for codeToType in codesToType:
      debug(f"Typing {codeToType} on keypad {keypad - 1}")
      newCodes = typeCode([codeToType], keypad - 1)
      print(f"Found {len(newCodes)} codes for {codeToType} on keypad {keypad}, first code: {newCodes[0]}")
      codes += newCodes
  else:
    codes += codesToType

  debug(f"These are the new codes from {keypad - 1}: {codes}")

  options = []
  shortestCode = -1
  for code in codes:
    inFocus = 'A'
    toTypeForCode = ""
    for c in code:
      debug(f"Typing for {c} from {code} with focus {inFocus} on {keypad} ...")
      toType = tpyeIn(c, inFocus, keypad)
      debug(f"Typing for {c} from {code} with focus {inFocus} on {keypad} -> {toType}")
      inFocus = c
      toTypeForCode += toType

    print(f"toTypeForCode: {toTypeForCode}")
    allPermutations = permuteSequence(toTypeForCode, keypad)
    print(f"Found toTypeForCode = {toTypeForCode}, created permutations: {allPermutations}")
    for permutation in allPermutations:
      if isSequenceValid('A', permutation, keypad):
        debug(f"Valid: {permutation} on {keypad}")
        options.append(permutation)
        #print(f"Checking if {permutation} is the shortest option")
        if shortestCode == -1 or shortestCode > len(permutation):
          shortestCode = len(permutation)
      else:
        print(f"Invalid: {permutation} on {keypad}")

  shortestOptions = []
  for option in options:
    if len(option) == shortestCode and not option in shortestOptions:
      shortestOptions.append(option)

    debug(f"{shortestOptions} are the shortest options to type {codesToType} on {keypad}; overall were {len(options)} options found")
  print(f"Identified {len(shortestOptions)} shortest options out of {len(options)} valid options to type {codesToType} on {keypad}: {shortestOptions}")
  return shortestOptions

def complexity(code, toType):
  numericPart = ""
  for c in code:
    if c in ['0', '1','2','3','4','5','6','7','8','9']:
      numericPart += c
  debug(f"Numeric part in {code} is {numericPart}")
  return int(numericPart) * len(toType)

def validate(typedCode, keypad):
  debug(f"Validating {typedCode} on {keypad}")
  typedOnNextKeypad = ""
  inFocus = 'A'
  for c in typedCode:
    if c == 'A':
      typedOnNextKeypad += inFocus
    else:
      inFocus = changeFocus(inFocus, c, keypad)
      if not inFocus:
        print(f"Lost focus after typing {c} from {typedCode} on {keypad}!")

  if keypad > 1:
    return validate(typedOnNextKeypad, keypad - 1)
  else:
    return typedOnNextKeypad


def typeCodes(codes, keypad):
  toTypeForCodes = []
  for code in codes:
    print(f"OUTER: {code} from {codes}")
    toTypeOptions = typeCode([code], keypad)
    print(f"I need to type any of {toTypeOptions} for code {code}")
    
    for toType in toTypeOptions:
      if not validate(toType, keypad) == code:
        print(f"Unexpected result when typing in {toType}: {validate(toType, keypad)} (expected: {code})")
    toTypeForCodes.append(toTypeOptions)

  totalComplexity = 0
  for i in range(len(codes)):
    # use first code for complexity computation
    totalComplexity += complexity(codes[i], toTypeForCodes[i][0])

  return totalComplexity

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  codes = fetchData(DAY, useRealData)

  totalComplexity = typeCodes(codes, 4)

  print(f"Result for part 1: {str(totalComplexity)}")
  print(f"Expected:          126384")

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  codes = fetchData(DAY, useRealData)

  totalComplexity = typeCodes(codes, 4)

  print(f"Result for part 2: {str(totalComplexity)}")

def solve():
  seq = "<^<A"
  seq = "v<A<AA>>^AvAA^<A>Av<<A>>^AvA^Av<<A>>^AAv<A>A^A<A>Av<A<A>>^AAA<Av>A^A"
  #print(f"Permutations for {seq}: {permuteSequence(seq,3)}")
  part1(False)
  #part2(False)

  # likely best to start from scratch :-o