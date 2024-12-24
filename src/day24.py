DAY = "24"

from helper import DEBUG, debug, fetchData
from functools import lru_cache
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
        wireValues[wire] = wireValues[left] ^ wireValues[right]
      else:
        print(f"INVALID GATE for wire {wire}: gates[wire]")
        return
    else:
      # process gate later again
      gatesToProcess.append(wire)

def outputWiresToNumber(wireValues):
  debug(f"Selecting outputWires from {wireValues}")
  outputWires = []
  # pass 1 - ensure list has correct length
  for wire in wireValues.keys():
    if wire[0] == 'z':
      debug(f"Found output wire: {wire} with value {wireValues[wire]}")
      if not int(wire[1:]) in outputWires:
        for i in range(len(outputWires), int(wire[1:]) + 1):
          outputWires.append(0)

  # pass 2 - set bits
  for wire in wireValues.keys():
    if wire[0] == 'z':
        outputWires[len(outputWires) - 1 - int(wire[1:])] = wireValues[wire]
        debug(f"appended outputWires = {outputWires}")
  debug(f"outputWires = {outputWires}")
  
  binary = "0b"
  for o in outputWires:
    binary += str(o)
  debug(f"Binary representation: {binary}")
  return binary, int(binary, 2)
        

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)
  wireValues, gates = transform(input)

  simulate(wireValues, gates)

  debug(f"wireValues: {wireValues}")
  binary,number = outputWiresToNumber(wireValues)

  print(f"Result for part 1: {binary} ({number})") #    my binary: 0b000000000000001101101110
  print(f"Expected:            0011111101000 ({int("0b0011111101000",2)})") # correct binary:              0011111101000

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)
  wireValues, gates = transform(input)

  simulate(wireValues, gates)

  number = outputWiresToNumber(wireValues)

  print(f"Result for part 2: {number}")
  print(f"Expected:          {2024}")

def solve():
  part1(True)
  #part2(False)