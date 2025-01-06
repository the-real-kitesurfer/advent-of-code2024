DAY = "17"

from helper import DEBUG, debug, fetchData
from functools import lru_cache

registers = [0,0,0]
output = []
program = []
pointer = 0
exitOnJump = False

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

def operand(combo = True):
  if not combo or program[pointer + 1] < 4:
    return program[pointer + 1]
  if combo and  program[pointer + 1] == 4:
    return registers[0]
  if combo and program[pointer + 1] == 5:
    return registers[1]
  if combo and program[pointer + 1] == 6:
    return registers[2]
  print(f"OOPS - operand is {program[pointer + 1]}, combo: {combo}")

def adv():
  global registers
  global output
  global program
  global pointer

  #debug(f"adv - {registers[0]} // pow(2, {operand()}) ...")
  debug(f"adv - {registers[0]} // pow(2, {operand()}) = {registers[0] // pow(2, operand())}")
  registers[0] = registers[0] // pow(2, operand())

def bdv():
  global registers
  global output
  global program
  global pointer

  #debug(f"bdv - {registers[0]} // pow(2, {operand()}) ...")
  debug(f"bdv - {registers[0]} // pow(2, {operand()}) = {registers[0] // pow(2, operand())}")
  registers[1] = registers[0] // pow(2, operand())

def cdv():
  global registers
  global output
  global program
  global pointer

  #debug(f"cdv - {registers[0]} // pow(2, {operand()}) ...")
  debug(f"cdv - {registers[0]} // pow(2, {operand()}) = {registers[0] // pow(2, operand())}")
  registers[2] = registers[0] // pow(2, operand())

def jnz():
  global registers
  global output
  global program
  global pointer
  global exitOnJump

  debug(f"jnz - {registers[0]} == 0 = {registers[0] == 0}")
  if exitOnJump:
    exit()
  if registers[0] == 0:
    return False
  pointer = operand()
  return True

def bxl():
  global registers
  global output
  global program
  global pointer

  debug(f"bxl - {registers[1]} ^ {operand()} = {registers[1] ^ operand(False)}")
  registers[1] = registers[1] ^ operand(False)

def bxc():
  global registers
  global output
  global program
  global pointer

  debug(f"bxc - {registers[1]} ^ {registers[2]} = {registers[1] ^ registers[2]}")
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

  if pointer >= len(program):
    print(f"HALT - pointer {pointer} >= {len(program)} (len(program)")
    return False
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
  elif opsCode == 6:
      bdv()
  elif opsCode == 7:
      cdv()
  else:
      print(f"THIS SHOULD NOT HAVE HAPPENED - opsCode is {opsCode}. Oops ...")
      exit(-1)

  if not jumped:
    pointer += 2

  debug(f"DONE - Pointer: {pointer}, registers: {registers}, output: {output}")
  return True

def clonedItself(firstNChars):
  global output, program
  if not len(output) == firstNChars:
    debug(f"Length as-is {len(output)} != to-be {firstNChars}")
    return False
  for i in range(len(output)):
    if not output[i] == program[i]:
      #debug(f"{i}: {output[i]}, {program[i]}")
      debug(f"{output} vs {program} differ at index {i}")
      return False
  return True

def clonedItselfFromEnd(lastNChars):
  global output, program
  if not len(output) == lastNChars:
    debug(f"Length as-is {len(output)} != to-be {lastNChars}")
    return False
  for i in range(len(output) -1, -1, -1):
    if not output[len(output) - 1 - i] == program[len(program) - 1 - i]:
      #debug(f"{i}: {output[i]}, {program[i]}")
      debug(f"{output} vs {program} differ at index {i}")
      return False
  return True

def findRegAForOut(lowerBoundRegA, expectedOutput, lastOpsToSkip, lastNChars):
  inputRegA = lowerBoundRegA
  global output, pointer, program, registers
  proogram = program
  output = []
  while True:
    debug(f"Next try: {inputRegA} for {lastNChars}")

    output = []
    pointer = 0
    registers[0] = inputRegA
    registers[1] = 0
    registers[2] = 0

    while pointer < len(program) - lastOpsToSkip:
      process()
      debug(f"Evaluated program for inputRegA {inputRegA} resulting in output: {output}; new pointer: {pointer}, updated registers: {registers}")

    if output == [expectedOutput]: # check 1 - the char matches the expected output
      evaluate(inputRegA)
      if clonedItselfFromEnd(lastNChars): # check 2 - all prev. chars match the expected output as well!
        break
        

    inputRegA += 1 # else: try next value for RegA

  return inputRegA

def evaluate(regA):
  global output, pointer, program, registers
  output = []
  registers[0] = regA
  registers[1] = 0
  registers[2] = 0
  pointer = 0

  while pointer < len(program):
    if not process():
      break

  return

def findRegAThatClonesTheProgram():
  global exitOnJump, output, program, registers
  debug(f"Program: {program}")
  lowerBoundRegA = 0
  for i in range(len(program) - 1, -1, -1):
    debug(f"Finding RegA resulting in the output of {program[i]} (the {i+1}th code in {program}) ...")
    regAForOutput = findRegAForOut(lowerBoundRegA, program[i], 2, len(program) - i)
    if i == -1:
      exitOnJump = True
    evaluate(regAForOutput)

    print(f"RegA {regAForOutput} results in the output of {program[i]} (the {i+1}th code in {program}) and {output} overall")
    lowerBoundRegA = regAForOutput * 8
  
  evaluate(regAForOutput)

  if output == program:
    print(f"Tada - RegA = {regAForOutput} results in output ({output}) == program ({program})")
  else:
    print(f"Too bad - RegA = {regAForOutput} results in output ({output}) != program ({program})")

    print(f"as-is ({output})")
    print(f"to-be ({program})")
  return regAForOutput

  
def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)
  initialize(input)
  #registers[0] = 6

  #while pointer < len(program):
  #  process()

  evaluate(registers[0])

  print(f"Result for part 1: {output}")

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)
  initialize(input)

  findRegAThatClonesTheProgram()
  return

  global program
  global output
  global pointer

  initialInput = 281474977135029
  #upper:   281474977135029
  #current: 281474463788733
  #lower:    28147497713502
  # NEW     164541160582818
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
      print(f"Output of complete program matches the program's code: as-is {output} vs to-be {program}")
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