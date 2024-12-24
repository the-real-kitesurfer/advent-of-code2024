DAY = "17"

from helper import DEBUG, debug, fetchData
from functools import lru_cache

registers = [0,0,0]
output = []
program = []
pointer = 0

def initialize(input):
  global registers
  global output
  global program
  global pointer

  registers[0] = int(input[0].split(' ')[2])
  registers[1] = int(input[1].split(' ')[2])
  registers[2] = int(input[2].split(' ')[2])

  program = []
  for code in input[4].split(' ')[1].split(','):
    program.append(int(code))
  pointer = 0
  output = []

def operand():
  if program[pointer + 1] < 4:
    return program[pointer + 1]
  if program[pointer + 1] == 4:
    return registers[0]
  if program[pointer + 1] == 5:
    return registers[1]
  if program[pointer + 1] == 6:
    return registers[2]
  print(f"OOPS - operand is {program[pointer + 1]}")

def adv():
  global registers
  global output
  global program
  global pointer

  denom = pow(2, operand())
  if operand() == 5:
    denom = pow(2, registers[1])

  debug(f"adv - {registers[0]} // pow(2, {operand()}) = {registers[0] // denom}")
  registers[0] = registers[0] // pow(2, operand())

def cdv():
  global registers
  global output
  global program
  global pointer

  denom = pow(2, operand())
  if operand() == 5:
    denom = pow(2, registers[1])

  debug(f"adv - {registers[0]} // pow(2, {operand()}) = {registers[0] // denom}")
  registers[2] = registers[0] // pow(2, operand())

def jnz():
  global registers
  global output
  global program
  global pointer

  debug(f"jnz - {registers[0]} == 0 = {registers[0] == 0}")
  if registers[0] == 0:
    return False
  pointer = operand()
  return True

def bxl():
  global registers
  global output
  global program
  global pointer

  #debug(f"bxl - {operand()} % 8 = {operand() % 8}")
  registers[1] = registers[1] ^ program[pointer+1]

def bxc():
  global registers
  global output
  global program
  global pointer

  #debug(f"bxl - {operand()} % 8 = {operand() % 8}")
  registers[1] = registers[1] ^ registers[2]

def bst():
  global registers
  global output
  global program
  global pointer

  debug(f"bst - {operand()} % 8 = {operand() % 8}")
  registers[1] = (operand() % 8)

def out():
  global registers
  global output
  global program
  global pointer

  debug(f"out - {operand()} % 8 = {operand() % 8}")
  output.append(operand() % 8)

def process():
  global registers
  global output
  global program
  global pointer

  debug(f"PROCESSING {program[pointer]} - Pointer: {pointer}, registers: {registers}")

  jumped = False
  opsCode = program[pointer]
  if opsCode == 0:
      adv()
  elif opsCode == 1:
      bxl()
  elif opsCode == 2:
      bst()
  elif opsCode == 3:
      jumped = jnz()
  elif opsCode == 4:
      bxc()
  elif opsCode == 5:
      out()
  elif opsCode == 7:
      cdv()
  else:
      print(f"THIS SHOULD NOT HAVE HAPPENED - opsCode is {opsCode}. Oops ...")
      exit(-1)

  if not jumped:
    pointer += 2

  debug(f"DONE - Pointer: {pointer}, registers: {registers}, output: {output}")

def clonedItself(firstNChars):
  if not len(output) == firstNChars:
    debug(f"Length as-is {len(output)} != to-be {firstNChars}")
    return False
  for i in range(len(output)):
    if not output[i] == program[i]:
      #debug(f"{i}: {output[i]}, {program[i]}")
      debug(f"{output} vs {program} differ at index {i}")
      return False
  return True
  
def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)
  initialize(input)
  #registers[0] = 6

  while pointer < len(program):
    process()

  print(f"Result for part 1: {output}")

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)

  global program
  global output

  initialInput = 281474977135029
  #upper:   281474977135029
  #current: 281474463788733
  #lower:    28147497713502
  #initialInput = pow(8,16)
  initialInput = int("0b11111111111111111111111111111111111111111111101", 2)
  bestMatch = -1
  max_digits = 0
  while True:
    debug(f"Trying to clone with initialInput {initialInput}")
    initialize(input)
    registers[0] = initialInput
    debug(f"Checking: as-is {output} vs to-be {program}")

    while pointer < len(program):
      process()
      if not clonedItself(len(output)):
        if len(output) > bestMatch:
          bestMatch = len(output)
          print(f"Aborting for iteration {initialInput}. Output no longer matches the program's start: as-is {output} vs to-be {program}")
        break

    if clonedItself(len(program)):
      print(f"Output of complete program does not match the program's code: as-is {output} vs to-be {program}")
      break

    for i in range(16):
      if len(output) <= i or not program[i] == output[i]:
        break
    if i >= max_digits:
      print(f"First {i} digits of {len(output)} correct for {bin(initialInput)} ({initialInput})")
      max_digits = i
    #binary = bin(initialInput)
    initialInput -= 1
    #while not "10111101" == binary[len(binary) - 8:]:
    #  initialInput -= 1
    #  binary = bin(initialInput)

  print(f"Result for part 2: {initialInput}")

def solve():
  #part1(True)
  part2(True)