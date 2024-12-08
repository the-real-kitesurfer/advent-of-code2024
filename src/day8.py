DAY = "8"

from helper import debug

def fetchData(file):
  with open("./resources/" + file, 'r') as f:
    lines = f.readlines()
    listOfStrings=[]
    for i, line in enumerate(lines):
      listOfStrings.append(line[:-1])
  
  return listOfStrings

def transform(input):
  antennas = []
  for l, line in enumerate(input):
    for c, char in enumerate(line):
      if not char == '.' and not char == '\n':
        antennas.append((c, l, char))

  debug("antennas: " + str(antennas))

  return antennas

def isInCity(position, width, height):
  return position[0] >= 0 and position[1] >= 0 and position[0] < width and position[1] < height

def computeAntinodes1(antennas, width, height):
  antinodes = []
  for antenna in antennas:
    for distX in range(width):
      for distY in range(height):
        if distX == 0 and distY == 0:
          continue
        if (antenna[0] + distX, antenna[1] + distY, antenna[2]) in antennas:
          antinodes.append((antenna[0] - distX, antenna[1] - distY))
        if (antenna[0] + distX, antenna[1] - distY, antenna[2]) in antennas:
          antinodes.append((antenna[0] - distX, antenna[1] + distY))
        if (antenna[0] - distX, antenna[1] - distY, antenna[2]) in antennas:
          antinodes.append((antenna[0] + distX, antenna[1] + distY))
        if (antenna[0] - distX, antenna[1] + distY, antenna[2]) in antennas:
          antinodes.append((antenna[0] + distX, antenna[1] - distY))

  debug("Found " + str(len(antinodes)) + " antinodes overall")
  validAntinodes = []
  for antinode in antinodes:
    if isInCity(antinode, width, height) and not antinode in validAntinodes:
      validAntinodes.append(antinode)

  debug("From these, " + str(len(validAntinodes)) + " are valid")

  return validAntinodes

def computeAntinodes2(antennas, width, height):
  antinodes = []
  for antenna in antennas:
    for distX in range(width):
      for distY in range(height):
        if distX == 0 and distY == 0:
          continue
        multiplier = 0
        while isInCity((antenna[0] - multiplier * distX, antenna[1] - multiplier * distY), width, height) or isInCity((antenna[0] - multiplier * distX, antenna[1] + multiplier * distY), width, height) or isInCity((antenna[0] + multiplier * distX, antenna[1] + multiplier * distY), width, height) or isInCity((antenna[0] + multiplier * distX, antenna[1] - multiplier * distY), width, height):
          if (antenna[0] + distX, antenna[1] + distY, antenna[2]) in antennas:
            antinodes.append((antenna[0] - multiplier * distX, antenna[1] - multiplier * distY))
          if (antenna[0] + distX, antenna[1] - distY, antenna[2]) in antennas:
            antinodes.append((antenna[0] - multiplier * distX, antenna[1] + multiplier * distY))
          if (antenna[0] - distX, antenna[1] - distY, antenna[2]) in antennas:
            antinodes.append((antenna[0] + multiplier * distX, antenna[1] + multiplier * distY))
          if (antenna[0] - distX, antenna[1] + distY, antenna[2]) in antennas:
            antinodes.append((antenna[0] + multiplier * distX, antenna[1] - multiplier * distY))
          multiplier += 1

  debug("Found " + str(len(antinodes)) + " antinodes overall")
  validAntinodes = []
  for antinode in antinodes:
    if isInCity(antinode, width, height) and not antinode in validAntinodes:
      validAntinodes.append(antinode)

  debug("From these, " + str(len(validAntinodes)) + " are valid")

  return validAntinodes

def plotAntinodes(antinodes, width, height):
  for y in range(height):
    row = ''
    for x in range(width):
      if (x, y) in antinodes:
        row += '#'
      else:
        row += '.'
    print(row)

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  if useRealData:
    input = fetchData('day' + DAY + '.txt')
  else:
    input = fetchData('sample' + DAY + '.txt')

  print ("Transforming data")
  antennas = transform(input)

  print("Computing antinodes")
  antinodes = computeAntinodes1(antennas, len(input[0]), len(input))

  plotAntinodes(antinodes, len(input[0]), len(input))

  print("Result for part 1: " + str(len(antinodes)))

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  if useRealData:
    input = fetchData('day' + DAY + '.txt')
  else:
    input = fetchData('sample' + DAY + '.txt')

  print ("Transforming data")
  antennas = transform(input)

  print("Computing antinodes")
  antinodes = computeAntinodes2(antennas, len(input[0]), len(input))

  plotAntinodes(antinodes, len(input[0]), len(input))

  print("Result for part 2: " + str(len(antinodes)))


def solve():
  #part1(True)
  part2(True)