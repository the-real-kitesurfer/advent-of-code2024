DAY = "7"

from helper import debug

def fetchData(file):
  with open("./resources/" + file, 'r') as f:
    lines = f.readlines()
    listOfStrings=[]
    for i, line in enumerate(lines):
      listOfStrings.append(line[:-1])
  
  return listOfStrings

def transform(input):
  equations = []
  for line in input:
    splitLine = line.split(":")
    testValues = []
    for number in splitLine[1].split(" "):
      if not number == '':
        testValues.append(number)
    equations.append([int(splitLine[0]), testValues])

  debug("equations: " + str(equations))
  return equations

def countValidCombinations(testValue, partialResult, numbers, useThirdOperator):
  if len(numbers) == 0:
    if testValue == partialResult:
      return 1
    else:
      return 0

  if partialResult > testValue:
    return 0

  if useThirdOperator:
    return countValidCombinations(testValue, int(str(partialResult) + numbers[0]), numbers[1:], useThirdOperator) + countValidCombinations(testValue, partialResult + int(numbers[0]), numbers[1:], useThirdOperator) + countValidCombinations(testValue, partialResult * int(numbers[0]), numbers[1:], useThirdOperator)
  else:
    return countValidCombinations(testValue, partialResult + int(numbers[0]), numbers[1:], useThirdOperator) + countValidCombinations(testValue, partialResult * int(numbers[0]), numbers[1:], useThirdOperator)

def findValidEquations(equations, useThirdOperator):
  validEquations = []
  for equation in equations:
    if countValidCombinations(equation[0], 0, equation[1], useThirdOperator) > 0:
      validEquations.append(equation)
  return validEquations

def sumOfTestValues(equations):
  sum = 0
  for equation in equations:
    sum += equation[0]
  return sum

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  if useRealData:
    input = fetchData('day' + DAY + '.txt')
  else:
    input = fetchData('sample' + DAY + '.txt')

  print("Transforming input")
  equations = transform(input)

  print ("Finding valid equations")
  validEquations = findValidEquations(equations, False)

  print("Found " + str(len(validEquations)) + " valid equations")
  
  print("Result for part 1: " + str(sumOfTestValues(validEquations)))

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  if useRealData:
    input = fetchData('day' + DAY + '.txt')
  else:
    input = fetchData('sample' + DAY + '.txt')

  print("Transforming input")
  equations = transform(input)

  print ("Finding valid equations")
  validEquations = findValidEquations(equations, True)

  print("Found " + str(len(validEquations)) + " valid equations: "+ str(validEquations))
  
  print("Result for part 2: " + str(sumOfTestValues(validEquations)))

def solve():
  part1(True)
  part2(True)