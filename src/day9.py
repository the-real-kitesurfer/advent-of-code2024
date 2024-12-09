DAY = "9"

from helper import debug

def fetchData(file):
  with open("./resources/" + file, 'r') as f:
    lines = f.readlines()
    listOfStrings=[]
    for i, line in enumerate(lines):
      listOfStrings.append(line[:-1])
  
  return listOfStrings

def moveBlockByBlock(input):
  blocks = []
  fileId = 0
  isFile = True
  for c, char in enumerate(input[0]):
    for f in range(int(char)):
      if isFile:
        blocks.append(fileId)
      else:
        blocks.append(-1)
    if isFile:
      fileId += 1
    isFile = not isFile

  debug("Initial blocks: " + str(blocks))

  updatedBlocks = []
  sourceIndexForCopy = len(blocks) - 1
  for b, block in enumerate(blocks):
    debug("Processing block " + str(block))
    if b > sourceIndexForCopy:
      updatedBlocks.append(-1)
    elif block >= 0:
      updatedBlocks.append(block)
    else:
      debug("Copying block " + str(blocks[sourceIndexForCopy]))
      updatedBlocks.append(blocks[sourceIndexForCopy])
      sourceIndexForCopy -= 1
      while blocks[sourceIndexForCopy] == -1:
        sourceIndexForCopy -= 1
      debug("New sourceIndexForCopy: " + str(sourceIndexForCopy))

  debug("Updated blocks: " + str(updatedBlocks))

  return updatedBlocks

def numberBlocksWithId(blocks, start, reverse):
  result = 0
  direction = 1
  if reverse:
    direction = -1
  while blocks[start + direction * result] == blocks[start]:
    result += 1
    if start + direction * result < 0 or start + direction * result >= len(blocks):
      break

  return result

def moveEntireFiles(input):
  blocks = []
  fileId = 0
  isFile = True
  lengthPerFile = []
  firstIndexPerFile = []
  for c, char in enumerate(input[0]):
    if isFile:
      firstIndexPerFile.append(len(blocks))
    for f in range(int(char)):
      if isFile:
        blocks.append(fileId)
      else:
        blocks.append(-1)
    if isFile:
      lengthPerFile.append(int(char))
      fileId += 1
    isFile = not isFile

  debug("Initial blocks: " + str(blocks))

  updatedBlocks = []
  for block in blocks:
    updatedBlocks.append(block)
  sourceIndexForCopy = len(blocks) - 1
  processedBlocks = []

  nextFileToCopy = len(lengthPerFile) - 1
  checks = 0
  while nextFileToCopy > 0:
    debug("Finding a new place for " + str(nextFileToCopy))
    checks += 1
    print("Round " + str(checks))

    for i in range(len(blocks)):
      if i >= firstIndexPerFile[nextFileToCopy]:
        break
      if updatedBlocks[i] == -1:
        debug("Found " + str(numberBlocksWithId(updatedBlocks, i, False)) + " free blocks starting at " + str(i) + ", needing " + str(numberBlocksWithId(updatedBlocks, firstIndexPerFile[nextFileToCopy], False)) + " for fileId " + str(nextFileToCopy))
        if numberBlocksWithId(updatedBlocks, i, False) >= numberBlocksWithId(updatedBlocks, firstIndexPerFile[nextFileToCopy], False):
          for k in range(len(updatedBlocks)):
            if updatedBlocks[k] == nextFileToCopy:
              updatedBlocks[k] = -1
          for j in range(lengthPerFile[nextFileToCopy]):
            updatedBlocks[i + j] = nextFileToCopy
          firstIndexPerFile[nextFileToCopy] = i
          break
    nextFileToCopy -= 1
    # debug("Updated blocks: " + str(updatedBlocks))

  debug("Updated blocks: " + str(updatedBlocks))

  return updatedBlocks

def checksum(fileblocks):
  result = 0
  for b, block in enumerate(fileblocks):
    if block > 0:
      result += b * block

  return result

def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  if useRealData:
    input = fetchData('day' + DAY + '.txt')
  else:
    input = fetchData('sample' + DAY + '.txt')

  print ("Transforming data")
  fileblocks = moveBlockByBlock(input)

  print("Computing checksum")

  print("Result for part 1: " + str(checksum(fileblocks)))

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  if useRealData:
    input = fetchData('day' + DAY + '.txt')
  else:
    input = fetchData('sample' + DAY + '.txt')

  print ("Transforming data")
  fileblocks = moveEntireFiles(input)

  print("Computing checksum")

  print("Result for part 2: " + str(checksum(fileblocks)))

def solve():
  #part1(True)
  part2(True)