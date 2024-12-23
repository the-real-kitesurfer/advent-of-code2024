DAY = "13"

from helper import DEBUG, debug, fetchData

from math import gcd

def solve_diophantine(a, b, n):
    g = gcd(a, b)
    if n % g != 0:
        return None  # Keine Lösung
    # Erweiterten euklidischen Algorithmus nutzen
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        g, x1, y1 = extended_gcd(b, a % b)
        x, y = y1, x1 - (a // b) * y1
        return g, x, y

    g, x, y = extended_gcd(a, b)
    x0, y0 = x * (n // g), y * (n // g)
    # Allgemeine Lösung:
    return x0, y0, b // g, a // g

def example():
  a, b, n = 42, 17, 100
  solution = solve_diophantine(a, b, n)
  if solution:
    x0, y0, delta_x, delta_y = solution
    print(f"Lösung: x = {x0} + t * {delta_x}, y = {y0} - t * {delta_y}")
    print(f"Für t=1: x = {x0+delta_x}, y = {y0-delta_y} = {42*(x0+delta_x)+17*(y0-delta_y)}")
  else:
    print("Keine Lösung")

def transform(input):
  machines = []
  machineDetails = []
  for row in input:
    parts = row.split(" ")
    debug("Split " + row + " into " + str(parts))
    if len(parts) > 1:
      if parts[0] == 'Button':
        machineDetails.append(int(parts[2][2:len(parts[2]) - 1]))
        machineDetails.append(int(parts[3][2:]))
      else:
        machineDetails.append(int(parts[1][2:len(parts[1]) - 1]))
        machineDetails.append(int(parts[2][2:]))
        machines.append(machineDetails)
        debug("machineDetails: " + str(machineDetails))
        machineDetails = []

  return machines

def correctPrizePosition(machine):
  machine[4] += 10000000000000
  machine[5] += 10000000000000
  return machine

def win(machine):
  tokensSpent = 0
  for btnA in range(0, min(int(machine[4] / machine[0]), int(machine[5] / machine[1]))):
    for btnB in range(0, min(int(machine[4] / machine[2]), int(machine[5] / machine[3]))):
      debug("btnA: " + str(btnA) + "btnB: " + str(btnB) + "; x = " + str(btnA * machine[0] + btnB * machine[2]) + "/" + str(machine[4]))
      if btnA * machine[0] + btnB * machine[2] == machine[4] and btnA * machine[1] + btnB * machine[3] == machine[5]:
        return 3*btnA + btnB
      if btnA * machine[0] + btnB * machine[2] > machine[4] or btnA * machine[1] + btnB * machine[3] > machine[5]:
        break
  return 0

def winFast(machine):
  tokensSpent = 0
  check = 0
  for btnA in range(0, min(int(machine[4] / machine[0]), int(machine[5] / machine[1]))):
    if check % 1000000 == 0:
      print(f"Check {check/min(int(machine[4] / machine[0]), int(machine[5] / machine[1]))}")
    check += 1
    btnB = int((machine[4]-btnA*machine[0]) / machine[2])
    debug("btnA: " + str(btnA) + " / " + str(min(int(machine[4] / machine[0]), int(machine[5] / machine[1]))))
    if btnA * machine[0] + btnB * machine[2] == machine[4] and btnA * machine[1] + btnB * machine[3] == machine[5]:
      print(f"Solution: btnA={btnA}, btnB={btnB}")
      return 3*btnA + btnB
  return 0

def isValid(machine, btnA, btnB, both):
  if both:
    return btnA * machine[0] + btnB * machine[2] == machine[4] and btnA * machine[1] + btnB * machine[3] == machine[5]
  else:
    return btnA * machine[0] + btnB * machine[2] == machine[4] or btnA * machine[1] + btnB * machine[3] == machine[5]

def computeResultForX(machine, btnA, btnB):
  return btnA * machine[0] + btnB * machine[2]

def computeResultForY(machine, btnA, btnB):
  return btnA * machine[1] + btnB * machine[3]

def drillIn(machine, lowerBoundTX, upperBoundTX, x0X, delta_xX, y0X, delta_yX):
    t = lowerBoundTX
    btnA = x0X+t*delta_xX
    btnB = y0X-t*delta_yX
    oneAbove = False
    oneBelow = False

    resultForY = computeResultForY(machine, btnA, btnB)
    if resultForY == machine[5]:
      print("TADA - solved!")
    if resultForY < machine[5]:
      print("resultForY BELOW value for LOWER bound x")
      oneBelow = True
    elif resultForY > machine[5]:
      print("resultForY ABOVE value for LOWER bound x")
      oneAbove = True

    t = upperBoundTX
    btnA = x0X+t*delta_xX
    btnB = y0X-t*delta_yX

    resultForY = computeResultForY(machine, btnA, btnB)
    if resultForY == machine[5]:
      print("TADA - solved!")
      return 3* btnA + btnB
    if resultForY < machine[5]:
      print("resultForY BELOW value for UPPER bound x")
      oneBelow = True
    elif resultForY > machine[5]:
      print("resultForY ABOVE value for UPPER bound x")
      oneAbove = True

    if not oneAbove or not oneBelow:
      print("Can't be solved.")
      return 0

    if upperBoundTX - lowerBoundTX < 2:
      print("Upper - Lower bound < 2")
      return 0

    print(f"Solving left side: {lowerBoundTX}, {lowerBoundTX + (upperBoundTX - lowerBoundTX) // 2}")
    leftSolution = drillIn(machine, lowerBoundTX, lowerBoundTX + (upperBoundTX - lowerBoundTX) // 2, x0X, delta_xX, y0X, delta_yX)
    print(f"Solving right side: {lowerBoundTX + (upperBoundTX - lowerBoundTX) // 2}, {upperBoundTX}")
    rightSolution = drillIn(machine, lowerBoundTX + (upperBoundTX - lowerBoundTX) // 2, upperBoundTX, x0X, delta_xX, y0X, delta_yX)

    if leftSolution:
      print("Solved for left !")
      return leftSolution
    if rightSolution:
      print("Solved for right !")
      return rightSolution
    print("Odd - neither solved for left nor for right ...")
    return 0

def winFast2(machine):
  # Beispiel
  aX, bX, nX = machine[0], machine[2], machine[4]
  solutionX = solve_diophantine(aX, bX, nX)
  aY, bY, nY = machine[1], machine[3], machine[5]
  solutionY = solve_diophantine(aY, bY, nY)
  lastComp = 0
  numberTsTried = 0
  if solutionX and solutionY:
    x0X, y0X, delta_xX, delta_yX = solutionX
    x0Y, y0Y, delta_xY, delta_yY = solutionY
    print(f"Solution for x-axis: x = {x0X} + t * {delta_xX}, y = {y0X} - t * {delta_yX}")
    print(f"Solution for y-axis: x = {x0Y} + t * {delta_xY}, y = {y0Y} - t * {delta_yY}")
    lowerBoundTX = -x0X/delta_xX
    upperBoundTX = y0X/delta_yX
    lowerBoundTY = -x0Y/delta_xY
    upperBoundTY = y0Y/delta_yY

    if lowerBoundTX > upperBoundTX: 
      print("Not solveable for x-axis")
      return 0
    if lowerBoundTY > upperBoundTY: 
      print("Not solveable for y-axis")
      return 0

    print(f"X-axis is solveable for {lowerBoundTX} <= t >= {upperBoundTX}")
    print(f"Y-axis is solveable for {lowerBoundTY} <= t >= {upperBoundTY}")

    # check: if both the lower and upper bound result yield a too high / too low result for the other axis, we can skip
    t = lowerBoundTX
    btnA = x0X+t*delta_xX
    btnB = y0X-t*delta_yX
    oneAbove = False
    oneBelow = False

    resultForY = computeResultForY(machine, btnA, btnB)
    if resultForY == machine[5]:
      print("TADA - solved!")
    if resultForY < machine[5]:
      print("resultForY BELOW value for LOWER bound x")
      oneBelow = True
    elif resultForY > machine[5]:
      print("resultForY ABOVE value for LOWER bound x")
      oneAbove = True

    t = upperBoundTX
    btnA = x0X+t*delta_xX
    btnB = y0X-t*delta_yX

    resultForY = computeResultForY(machine, btnA, btnB)
    if resultForY == machine[5]:
      print("TADA - solved!")
    if resultForY < machine[5]:
      print("resultForY BELOW value for UPPER bound x")
      oneBelow = True
    elif resultForY > machine[5]:
      print("resultForY ABOVE value for UPPER bound x")
      oneAbove = True

    if not oneAbove or not oneBelow:
      print("Can't be solved.")
      return 0

    solution = drillIn(machine, int(lowerBoundTX) -1, int(upperBoundTX) +1, x0X, delta_xX, y0X, delta_yX)
    if solution:
      return solution
    else:
      return 0

    for t in range(int(lowerBoundTX) - 1, int(upperBoundTX) + 1):
      numberTsTried += 1
      if numberTsTried % 10000000 == 0:
        print(f"Check #{numberTsTried/(int(upperBoundTX) - int(lowerBoundTX))}: t={t}")
      btnA = x0X+t*delta_xX
      btnB = y0X-t*delta_yX

      resultForY = computeResultForY(machine, btnA, btnB)
      if resultForY == machine[5]:
        debug(f"Found t={t}: btnA={btnA}, btnB={btnB}")
        result = 3 * btnA + btnB 
        if result > 0:
          debug(f"---- TADA ----")
          return result

  debug("No solution found for y-axis")
  return 0

    
def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)
  machines = transform(input)

  tokensSpent = 0
  for machine in machines:
    tokensSpent += winFast2(machine)
    if winFast2(machine) > 0:
      print("Won machine " + str(machine))
      #break

  print("Result for part 1: " + str(tokensSpent))

def part2(useRealData):
  print("Day " + DAY + ", Part 2")
  #example()
  #return

  input = fetchData(DAY, useRealData)
  machines = transform(input)
  machineCnt = 0

  tokensSpent = 0
  for machine in machines:
    machine = correctPrizePosition(machine)
    print("Updated machine: " + str(machine))

    tokensSpent += winFast2(machine)
    machineCnt += 1
    print("Played machine " + str(machineCnt) + " out of " + str(len(machines)) + ", tokens spent already: " + str(tokensSpent))

  print("Result for part 2: " + str(tokensSpent))


def solve():
  part1(True)
  part2(True)