import itertools
DAY = "5"

def fetchData(file):
  with open("./resources/" + file, 'r') as f:
    lines = f.readlines()
    listOfStrings=[]
    for i, line in enumerate(lines):
      #print(line)
      listOfStrings.append(line[:-1])
  
  return listOfStrings

def transform(input):
  rules = []
  manuals = []
  extractRules = True
  for line in input:
    if line == "":
      extractRules = False
    elif extractRules:
      rules.append(line.split("|"))
    else:
      manuals.append(line.split(","))

  print("Found " + str(len(rules)) + " rules and " + str(len(manuals)) + " manuals")
  return rules, manuals

def isEntryValid(l, r, rules):
  for rule in rules:
    if r == rule[0] and l == rule[1]:
      #print("Pair " + str(l) + ", " + str(r) + " violates rule " + str(rule) + "!")  
      return False
  
  #print("Pair " + str(l) + ", " + str(r) + " complies with rule " + str(rule) + ".")  
  return True

def isManualValid(manual, rules):
  valid = True
  for i in range(len(manual)):
    # check "i" fulfills the rules with all its LEFT neightbours
    for l in range(i):
      if not isEntryValid(manual[l], manual[i], rules):
        valid = False
        break
    if not valid:
      break

    # check "i" fulfills the rules with all its RIGHT neightbours
    for r in range(len(manual) - i):
      if not isEntryValid(manual[i], manual[i + r], rules):
        valid = False
        break
    if not valid:
      break
  return valid

def extractManuals(manuals, rules, extractValid):
  filteredManuals = []
  for manual in manuals:
    valid = isManualValid(manual, rules)
    if extractValid and valid:
      filteredManuals.append(manual)
    if not extractValid and not valid:
      filteredManuals.append(manual)

  print("Filtered " + str(len(filteredManuals)) + " manuals")
  return filteredManuals

def fixInvalidManualsPerm(manuals, rules):
  fixedManuals = []
  invalidManuals = []
  for manual in manuals:
    print("Trying to fix manual " + str(manual) + " ...")
    fixed = False
    for perm in list(itertools.permutations(manual)):
      if isManualValid(perm, rules):
        fixed = True
        print("Fixed manual " + str(manual) + ": " + str(perm))
        fixedManuals.append(perm)
        break
    if not fixed:
      print("Failed to fix " + str(manual))
      invalidManuals.append(manual)

  print("Fixed " + str(len(fixedManuals)) + " manuals, " + str(len(invalidManuals)) + " remain invalid")
  return fixedManuals

def fixInvalidManuals(manuals, rules):
  fixedManuals = []
  invalidManuals = []
  for manual in manuals:
    fixed, fixedManual = fixInvalidManual(manual, rules)
    if fixed:
      print("Fixed manual " + str(manual) + ": " + str(fixedManual))
      fixedManuals.append(fixedManual)
    else:
      print("Failed to fix " + str(manual))
      invalidManuals.append(manual)

  print("Fixed " + str(len(fixedManuals)) + " manuals, " + str(len(invalidManuals)) + " remain invalid")
  return fixedManuals


def fixInvalidManualPerm(manual, rules):
  print("Trying to fix manual " + str(manual) + " ...")
  for perm in list(itertools.permutations(manual)):
    if isManualValid(perm, rules):
      return True, perm
  return False, []

def fixInvalidManual(manual, rules):
  if isManualValid(manual, rules):
    return True, manual
  print("Trying to fix manual " + str(manual) + " ...")

  leftPart = getNeighbours(manual[0], manual[1:], rules, True)
  rightPart = getNeighbours(manual[0], manual[1:], rules, False)

  fixedLeft, leftManual = fixInvalidManual(leftPart, rules)
  fixedRight, rightManual = fixInvalidManual(rightPart, rules)

  fixedManual = []
  for m in leftManual:
    fixedManual.append(m)
  fixedManual.append(manual[0])
  for m in rightManual:
    fixedManual.append(m)
  return fixedLeft and fixedRight, fixedManual

def getNeighbours(entry, manual, rules, findLeftNeightbours):
  neighbours = []
  matchingRules = []
  for r in rules:
    if findLeftNeightbours and r[1] == entry:
      matchingRules.append(r[0])
    if not findLeftNeightbours and r[0] == entry:
      matchingRules.append(r[1])


  print("Found these matching rules for entry " + str(entry) + ": " + str(matchingRules) + ", findLeftNeightbours=" + str(findLeftNeightbours))
  for r in matchingRules:
    #print("Checking: is " + str(r) + " in " + str(manual) + ": " + str(r in manual))
    if r in manual:
      neighbours.append(r)
  return neighbours

def sumOfCenter(manuals):
  sum = 0
  for manual in manuals:
    sum += int(manual[int(len(manual) / 2)])

  return sum

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  if useRealData:
    input = fetchData('day' + DAY + '.txt')
  else:
    input = fetchData('sample' + DAY + '.txt')

  print ("Transforming data")
  rules, manuals = transform(input)

  print("Extracting valid manuals")
  validManuals = extractManuals(manuals, rules, True)
  print("Result for part 1: " + str(sumOfCenter(validManuals)))

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  if useRealData:
    input = fetchData('day' + DAY + '.txt')
  else:
    input = fetchData('sample' + DAY + '.txt')

  print ("Transforming data")
  rules, manuals = transform(input)

  print("Extracting invalid manuals")
  invalidManuals = extractManuals(manuals, rules, False)

  fixedManuals = fixInvalidManuals(invalidManuals, rules)

  print("Result for part 1: " + str(sumOfCenter(fixedManuals)))

def solve():
  part1(True)
  part2(True)