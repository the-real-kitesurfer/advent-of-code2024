DAY = "24"

from helper import DEBUG, debug, fetchData
from functools import lru_cache
import random
import itertools

def transform(input):
  wireValues = {}
  gates = {}

  for line in input:
    if len(line) > 0:
      if len(line.split(": ")) == 2:
        wireValues[line.split(": ")[0]] = int(line.split(": ")[1])
      else:
        gates[line.split(" -> ")[1]] = (line.split(" ")[0], line.split(" ")[1], line.split(" ")[2])

  debug(f"wireValues: {wireValues}")
  debug(f"gates: {gates}")

  return wireValues, gates

def simulate(wireValues, gates):
  gatesToProcess = []
  for wire in gates.keys():
    gatesToProcess.append(wire)
  
  while len(gatesToProcess):
    debug(f"{len(gatesToProcess)} gates to process")
    wire = gatesToProcess.pop(0)
    left = gates[wire][0]
    op = gates[wire][1]
    right = gates[wire][2]
    debug(f"Checking: {left} and {right} in {wireValues.keys()}")
    if left in wireValues.keys() and right in wireValues.keys():
      if op == "AND":
        wireValues[wire] = wireValues[left] & wireValues[right]
      elif op == "OR":
        wireValues[wire] = wireValues[left] | wireValues[right]
      elif op == "XOR":
        if wire == "z00": debug(f"{wire} with left={left} and right={right} = {wireValues[left]} XOR {wireValues[right]} = {wireValues[left] ^ wireValues[right]}")
        wireValues[wire] = wireValues[left] ^ wireValues[right]
      else:
        print(f"INVALID GATE for wire {wire}: gates[wire]")
        return
    else:
      # process gate later again
      gatesToProcess.append(wire)

def wiresToNumber(wireValues, c):
  debug(f"Selecting outputWires from {wireValues}")
  outputWires = []
  # pass 1 - ensure list has correct length
  for wire in wireValues.keys():
    if wire[0] == c:
      debug(f"Found output wire: {wire} with value {wireValues[wire]}")
      if not int(wire[1:]) in outputWires:
        for i in range(len(outputWires), int(wire[1:]) + 1):
          outputWires.append(0)

  # pass 2 - set bits
  for wire in wireValues.keys():
    if wire[0] == c:
        outputWires[int(wire[1:])] = wireValues[wire]
        debug(f"appended outputWires = {outputWires}")
  debug(f"outputWires = {outputWires}")
  
  binary = "0b"
  number = 0
  debug(f"len: {len(outputWires)}")
  for i in range(len(outputWires)-1, -1, -1):
    o = outputWires[i]
    binary += str(o)
    debug(f"{number} + {o}*{pow(2,i)}")
    number += pow(2,i) * o
    debug(f"={number}")

  debug(f"Binary representation: {binary}, number: {number} vs {int(binary, 2)}")
  return binary, number
        

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)
  wireValues, gates = transform(input)

  simulate(wireValues, gates)

  debug(f"wireValues: {wireValues}")
  binary,number = wiresToNumber(wireValues, 'z')

  print(f"Result for part 1: {binary} ({number})") #    my binary: 0b000000000000001101101110
  print(f"Expected:            0011111101000 ({int("0b0011111101000",2)})") # correct binary:              0011111101000

def printGate(gates, gate):
  if gate[0][0] == 'x' or gate[0][0] == 'y':
    leftStr = gate[0]
  else:
    leftStr = printGate(gates, gates[gate[0]])
  if gate[2][0] == 'x' or gate[2][0] == 'y':
    rightStr = gate[2]
  else:
    rightStr = printGate(gates, gates[gate[2]])

  return "(" + leftStr + ') ' + gate[1] + ' (' + rightStr + ")"

def printGates(gates):
  printedGates = {}
  for wire in gates.keys():
    if wire[0] == 'z':
      printedGates[wire] = printGate(gates, gates[wire])
  #print(f"{printedGates}")
  return printedGates

def inputWiresForOutputWire(gates, gate):
  debug(f"inputWiresForOutputWire: {gate}")
  debug(f"gate[0]: {gate[0]}")
  debug(f"gate[2]: {gate[2]}")
  if gate == "w":
    exit()

  if gate[0][0] == 'x' or gate[0][0] == 'y':
    leftList = [gate[0]]
  else:
    leftList = [gate[0]] + inputWiresForOutputWire(gates, gates[gate[0]])

  if gate[2][0] == 'x' or gate[2][0] == 'y':
    rightList = [gate[2]]
  else:
    rightList = [gate[2]] + inputWiresForOutputWire(gates, gates[gate[2]])

  return leftList + rightList

def inputWiresForOutputWires(gates):
  result = {}
  for wire in gates.keys():
      debug(f"Checking wire {wire}")
      result[wire] = inputWiresForOutputWire(gates, gates[wire])
  return result

def isValidGate(printedGate, maxInputWire):
  for part in printedGate.split(" "):
    if part[0] in ['x', 'y']:
      if int(part[1:]) > maxInputWire:
        return False
  return True

def validateGates(printedGates):
  for i in range(50,-1,-1):
    if i < 10:
      outputWire = "z0" + str(i)
    else:
      outputWire = "z" + str(i)
    if outputWire in printedGates:
      if not isValidGate(printedGates[outputWire], int(outputWire[1:])):
        print(f"{outputWire} is INVALID")

def checkBinary(b1, b2):
  differences = []
  while len(b2) < len(b1):
    b2 = "0" + b2
  while len(b1) < len(b2):
    b1 = "0" + b1
  for i in range(len(b1)-1,-1,-1):
    if not b1[i] == b2[i]:
      debug(f"Difference in bit {len(b1)-1-i}: {b1[i]} vs {b2[i]}")
      differences.append(len(b1)-1-i)
  return differences

def swap(gates, w1, w2):
  if w1 == "xxx":
    return
  g1 = gates[w1]
  gates[w1] = gates[w2]
  gates[w2] = g1

def part2(useRealData):
  # attempt - "smart" swapping, based on the observation, that the 7th bit was the first "bad" one, and then keep on "forcing" to fix the next "bad" bit
  # basically worked right away, but I first concatenated the wires involved in the swapped expression (hence 16 ... :face-palm)
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)

  incorrectBits = []
  for i in range(50):
    incorrectBits.append(0)

  # idea: identify which gates influence which bit
  # outer loop: swap all gates that influences bit 7 against any other, and check that bits 0..7 are still/now correct
  # check that the swapped counterpart does not contain the output wire!
  wireValues, gates = transform(input)

  alwaysSwap = [("z07","shj"),("wkb","tpk"), ("z23","pfn"),("z27","kcd")] #bit 7, bit 23, bit 27, bit 
  alwaysSwap = [("z07","shj"),("wkb","tpk"), ("z23","pfn"),("z27","kcd")] #bit 7, bit 16, bit 23, bit -> z27,kcd to be checked
  #alwaysSwap = []
  doNotSwap = []

  for s in alwaysSwap:
    swap(gates, s[0], s[1])
    doNotSwap.append(s[0])
    doNotSwap.append(s[1])

  minGoodBits = 23
  checkPrefix = "0"
  if True or minGoodBits > 45:
    for n in range(100):
      wireValues, gates = transform(input)
      for s in alwaysSwap:
        swap(gates, s[0], s[1])

      if n > 0:
        for i in range(45):
          if i < 10:
            wireValues["x0" + str(i)] = random.choice([0,1])
            wireValues["y0" + str(i)] = random.choice([0,1])
          else:
            wireValues["x" + str(i)] = random.choice([0,1])
            wireValues["y" + str(i)] = random.choice([0,1])

    simulate(wireValues, gates)

    print(f"wireValues: {wireValues}")
    xBinary, xNumber = wiresToNumber(wireValues, 'x')
    yBinary, yNumber = wiresToNumber(wireValues, 'y')
    zBinary, zNumber = wiresToNumber(wireValues, 'z')

    # final (?) idee: find ALL options to fix bit 7; then find ALL options to fix the next bit; and two more times ... -> and ensure, that the later swaps do not influence the earlier ones!

    print(f"Result for part 2: {zBinary} ({zNumber})")
    print(f"Expected:            {'{0:08b}'.format(xNumber + yNumber)} ({xNumber + yNumber} = {xNumber} + {yNumber})")
    print(f"CHECK X:             0b{'{0:08b}'.format(xNumber)} ({xNumber})")
    print(f"CHECK2 X:            {xBinary} ({xNumber})")
    print(f"CHECK Y:             0b{'{0:08b}'.format(yNumber)} ({yNumber})")
    print(f"CHECK2 Y:            {yBinary} ({yNumber})")

    differences = checkBinary("0b"+'{0:08b}'.format(xNumber + yNumber), zBinary)
    firstBadBit = 100
    for diff in differences:
      if diff < firstBadBit:
        firstBadBit = diff
      incorrectBits[diff] = 1

    print(f"SOLVED BIT first {firstBadBit} bits!")
    #return

    affectedWires = []
    for s in alwaysSwap:
      affectedWires.append(s[0])
      affectedWires.append(s[1])
    affectedWires.sort()
    print(f"affectedWires: {affectedWires}")
    resultString = ""
    for w in affectedWires:
      resultString += w + ","
    print(resultString)
    return

  inputWsForOutputWs = inputWiresForOutputWires(gates)
  for i in range(46):
    if i < 10:
      infix = "0"
    else:
      infix = ""

    key = "z" + infix + str(i)
    print(f"# input wires for {key}: {len(inputWsForOutputWs[key])}")

  if False:
    return

  swaps = 0
  for g1 in gates:
    for g2 in gates:
      if swaps % 100 == 0:
        print(f"Swap {swaps} of approx {(314-92)*(314-92)}")
      swaps += 1
      if g1 == g2 or g1 in inputWsForOutputWs[g2] or g2 in inputWsForOutputWs[g1] or g1 in doNotSwap or g2 in doNotSwap:
        # skip no-ops and avoid recursion
        continue
      #if not g1 in inputWsForOutputWs["z" + checkPrefix + str(minGoodBits)] and not g2 in inputWsForOutputWs["z" + checkPrefix + str(minGoodBits)]:
      #  continue

      # do 10 random rounds and check which bits are incorrect
      notWorking = 0
      for n in range(100):
        if notWorking > 0:
          break
        wireValues, gates = transform(input)
        swap(gates, g1, g2)
        for s in alwaysSwap:
          swap(gates, s[0], s[1])

        if n > 0:
          for i in range(45):
            if i < 10:
              wireValues["x0" + str(i)] = random.choice([0,1])
              wireValues["y0" + str(i)] = random.choice([0,1])
            else:
              wireValues["x" + str(i)] = random.choice([0,1])
              wireValues["y" + str(i)] = random.choice([0,1])

        if False:
          printedGates = printGates(gates)
          
          print(f"x00: {wireValues["x00"]}")
          print(f"y00: {wireValues["y00"]}")
          print(f"z00: {printedGates["z00"]}")
          print(f"z01: {printedGates["z01"]}")
          print(f"z02: {printedGates["z02"]}")
          print(f"z03: {printedGates["z03"]}")
          print(f"z04: {printedGates["z04"]}")
          print(f"z05: {printedGates["z05"]}")
          if "z06" in printedGates: print(f"z06: {printedGates["z06"]}")
          if "z07" in printedGates: print(f"z07: {printedGates["z07"]}")
          #print(f"z08: {printedGates["z08"]}")
          #print(f"z09: {printedGates["z09"]}")

          validateGates(printedGates)

          #return

        xBinary, xNumber = wiresToNumber(wireValues, 'x')
        yBinary, yNumber = wiresToNumber(wireValues, 'y')

        debug(f"Doing round {n} after swapping {g1} and {g2}")
        debug(f"inputWsForOutputWs for {g1}: {inputWsForOutputWs[g1]}")
        debug(f"inputWsForOutputWs for {g2}: {inputWsForOutputWs[g2]}")
        simulate(wireValues, gates)

        debug(f"wireValues: {wireValues}")
        zBinary, zNumber = wiresToNumber(wireValues, 'z')

        differences = checkBinary("0b"+'{0:08b}'.format(xNumber + yNumber), zBinary)
        firstBadBit = 100
        for diff in differences:
          if diff < firstBadBit:
            firstBadBit = diff
          incorrectBits[diff] = 1

        if firstBadBit > minGoodBits:
          debug(f"SOLVED BIT first {firstBadBit} bits! Swap: {g1} vs {g2}")
          #return
        else:
          # early out - next n rounds will not help!
          debug(f"Only first {firstBadBit} bits done for this swap: {g1} vs {g2}")
          notWorking += 1
          #break

        if DEBUG:
          print(f".                    5432109876543210987654321098765432109876543210")
          print(f"Result for part 2: {zBinary} ({zNumber})")
          print(f"Expected:            {'{0:08b}'.format(xNumber + yNumber)} ({xNumber} + {yNumber} = {xNumber + yNumber})")
          print(f"CHECK X:             0b{'{0:08b}'.format(xNumber)} ({xNumber})")
          print(f"CHECK2 X:            {xBinary} ({xNumber})")
          print(f"CHECK Y:             0b{'{0:08b}'.format(yNumber)} ({yNumber})")
          print(f"CHECK2 Y:            {yBinary} ({yNumber})")
          print(f"XORed X:             {int("0b110100100010101111011111110110111111010101111",2)} ({xNumber + yNumber})")
          print(f"XORed X:             {int("0b110100001101011000000111101010110010000011111",2)} ({xNumber + yNumber})")
          print(f"XORed Z:             {int("0b000000101111110111011000011100001101010111000",2)} ({xNumber + yNumber})")

          #b1 = "0110100101111100100011100001100011111000101110"
          #b2 = "110100101111100011011100001010011111000101110"
          #print(f"DIFFERENCES {b1} vs {b2}")
          #checkBinary(b1, b2)

      if notWorking == 0:
        print(f"SOLVED for first {minGoodBits} bits: swapping {g1} and {g2}")
        return

      if DEBUG:
        for i in range(50):
          if incorrectBits[i] > 0:
            print(f"Bit {i} is incorrect")


def solve():
  #part1(True)
  part2(True)

#Result for part 2:   0b1001000101001100110000010110110100001100110000 (39939712172848)
#Expected:            0b0101010111101110001110110100011111111110111101 (20188256888737 + 3432164399132 = 23620421287869)
#CHECK X:             0b0100100101110001110001111000010110011110100001 (20188256888737)
#CHECK2 X:            0b0100100101110001110001111000010110011110100001 (20188256888737)
#CHECK Y:             0b0000110001111100011100111100001001100000011100 (3432164399132)
#CHECK2 Y:            0b0000110001111100011100111100001001100000011100 (3432164399132)

# (y00 AND x00) XOR (x01 XOR y01)

# 