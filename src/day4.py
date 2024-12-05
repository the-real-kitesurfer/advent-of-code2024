DAY = "4"

def fetchData(file):
  with open("./resources/" + file, 'r') as f:
    lines = f.readlines()
    listOfStrings=[]
    for i, line in enumerate(lines):
      #print(line)
      listOfStrings.append(line)
  
  return listOfStrings

def transform(input):
  grid =[]
  for line in input:
    row = []
    for char in line:
      row.append(char)
    grid.append(row)
  return grid

def mark(marked, new):
  for entry in new:
    marked[entry[1]][entry[0]] += 1

def prep(grid):
  marked =[]
  for line in grid:
    row = []
    for char in line:
      if (not char == '\n'):
        row.append(0)
    marked.append(row)
  return marked

def printMarked(marked):
  print("   0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ")
  print("  ==============================")
  for y, row in enumerate(marked):
    print(str(y) + "|" + str(row) + "|" + str(y))
  print("  ==============================")
  print("   0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ")

def count(word, grid, marked):
  count = 0

  #horizontally
  hCount = 0
  for y in range(len(grid)):
    for x in range(len(grid[y])- len(word) + 1):
      found = 1
      new = []
      for i, char in enumerate(word):
        new.append([x+i, y])
        if not grid[y][x+i] == char:
          found = 0
          #print("char " + char + " not found at " + str(x + i) + ": " + row[x+i])
          break
      count += found
      hCount += found
      if found:
        mark(marked, new)
        #print("Horizontally found " + word + " in " + str(x) + ", " + str(y) + ", marking " + str(new))

  # vertically
  vCount = 0
  #print("Vertical check: " + str(len(grid[0])) + "*" + str(len(grid)- len(word)+1) + ", inner loop: 0.." + str(len(word)))
  for x in range(len(grid[0])):
    for y in range(len(grid) - len(word) + 1):
      found = 1
      new = []
      for i, char in enumerate(word):
        new.append([x, y+i])
        #if (x==9) and ((y+i)==9):
        #  print("Checking char " + char + " at " + str(x) + ", " + str(y+1) + ": " + grid[y+i][x] + " --> " + str(grid[y+i][x] == char))
        if not grid[y+i][x] == char:
          found = 0
          #if (x==9) and ((y+i)==9):
          #  print("char " + char + " not found at " + str(x) + ", " + str(y+1) + ": " + grid[y+i][x] + " --> " + str(grid[y+i][x] == char))
          break
      count += found
      vCount += found
      if found:
        mark(marked, new)
        #print("Vertically found " + word + " in " + str(x) + ", " + str(y))

  # diagonally left ro right
  ltrCount = 0
  for xoffset in range(len(grid[0])-len(word) + 1):
    for yoffset in range(len(grid) - len(word) + 1):
      found = 1
      new = []
      for i, char in enumerate(word):
        new.append([xoffset+i,yoffset+i])
        if not grid[yoffset+i][xoffset+i] == char:
          found = 0
          #print("char " + char + " not found at " + str(start + i) + ": " + grid[start+i][col])
          break
      count += found
      ltrCount += found
      if found:
        mark(marked, new)
        #print("Diagonally ltr found " + word + " with start " + str(yoffset) + ", " + str(xoffset))

  #diagonally right to left
  rtlCount = 0
  #print("rtl check: " + str(len(grid[0])-len(word)) + "*" + str(len(grid) - len(word)) + ", inner loop: 0.." + str(len(word)))
  for xoffset in range(len(grid[0])-len(word)):
    for yoffset in range(len(grid) - len(word)+1):
      found = 1
      new = []
      for i, char in enumerate(word):
        #print("Checking " + str(xoffset+len(word)-i) + ", " + str(yoffset+i) + " against char " + str(char) + ": " + str(grid[yoffset+i][xoffset+len(word)-i]))
        #if (xoffset+len(word)-i)==4 and (yoffset+i)==6:
        #  print("i, char: " + str(i) + ", " + str(char))
        new.append([xoffset+len(word)-i-1, yoffset+i])
        if not grid[yoffset+i][xoffset+len(word)-i-1] == char:
          found = 0
          #print("char " + char + " not found at (" + str(xoffset+len(word)-i-1) + ", " + str(yoffset+i) + ") : " + grid[yoffset+i][xoffset+len(word)-i-1])
          break
      count += found
      rtlCount += found
      if found:
        mark(marked, new)
        #print("Diagonally rtl found " + word + " with start " + str(yoffset) + ", " + str(xoffset))
    
  print("Found " + str(hCount) + " hor, " + str(vCount) + " ver, " + str(ltrCount) + " ltr and " + str(rtlCount) + " rtl")
  
  printMarked(marked)
  return count, marked

def countXShape(word1, word2, grid, marked):
  count = 0

  for xoffset in range(len(grid[0]) - len(word1) + 1):
    for yoffset in range(len(grid) - len(word1) + 1):
      found = 1
      new = []
      for i, char1 in enumerate(word1):
        if char1 == 'A':
          new.append([xoffset+i,yoffset+i])
        if not grid[yoffset+i][xoffset+i] == char1 or not grid[yoffset+i][xoffset-i+2] == word2[i]:
          found = 0
          #print("char " + char + " not found at " + str(start + i) + ": " + grid[start+i][col])
          break
      count += found
      if found:
        mark(marked, new)
        #print("Found " + word1 + " and " + word2 + " around center " + str(xoffset+1) + ", " + str(yoffset+1) + ": " + str(grid[yoffset+1][xoffset+1]) + " -1/-1=" + str(grid[yoffset][xoffset+1]) + " +1/-1=" + str(grid[yoffset][xoffset+2]+ " +1/+1=" + str(grid[yoffset+2][xoffset+2])+ " -1/+1=" + str(grid[yoffset+2][xoffset])))
  
  printMarked(marked)
  return count, marked

def part1(useSample):
  print("Day " + DAY + ", Part 1")

  if useSample:
    input = fetchData('sample' + DAY + '.txt')
  else:
    input = fetchData('day' + DAY + '.txt')

  print ("Processing data")
  grid = transform(input)
  marked = prep(grid)

  print("Computing")
  result1, marked = count("XMAS", grid, marked)
  result2, marked = count("SAMX", grid, marked)
  print("Result: " + str(result1 + result2))

def part2(useSample):
  print("Day " + DAY + ", Part 2")


  if useSample:
    input = fetchData('sample' + DAY + '.txt')
  else:
    input = fetchData('day' + DAY + '.txt')

  print ("Processing data")
  grid = transform(input)
  marked = prep(grid)

  print("Computing")
  result1,marked = countXShape("MAS", "MAS", grid, marked)
  result2,marked = countXShape("MAS", "SAM", grid, marked)
  result3,marked = countXShape("SAM", "SAM", grid, marked)
  result4,marked = countXShape("SAM", "MAS", grid, marked)
  print("Result: " + str(result1 + result2 + result3 + result4))

def solve():
  #part1(False)
  part2(False)