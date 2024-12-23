DAY = "22"

from helper import DEBUG, debug, fetchData
from functools import lru_cache
import itertools

def transform(input):
  initialPrices = []
  for line in input:
    initialPrices.append(int(line))
  return initialPrices

def mix(n, m):
  debug(f"Mixing {n} and {m}: {n ^ m}")
  return n ^ m

def prune(m):
  debug(f"Prining {m}: {m % 16777216}")
  return m % 16777216

def nextNumber(n):
  m = n << 6 #*64
  m = mix(n, m)
  m = prune(m)
  debug(f"Step 1: {n} turned into {m}")

  n = m
  m = m >> 5 #//32
  m = mix(n, m)
  m = prune(m)
  debug(f"Step 2: {n} turned into {m}")

  n = m
  m = m << 11 #*2048
  m = mix(n, m)
  m = prune(m)
  debug(f"Step 3: {n} turned into {m}")

  return m

def computePricesForBuyer(initialPrice, count):
  prices = []
  n = initialPrice
  for i in range(count):
    m = nextNumber(n)
    debug(f"nextNumber for {n} is {m}")
    n = m
    prices.append(n)

  return prices

def computePrices(initialPrices, count):
  pricesPerBuyer = []
  for initialPrice in initialPrices:
    pricesPerBuyer.append([initialPrice] + computePricesForBuyer(initialPrice, count))
  return pricesPerBuyer

def sumUp(prices):
  sum = 0
  for l in prices:
    sum += l[len(l) - 1] # sum up last price per buyer
  return sum

def pricesToChangeSequence(prices):
  changeSequence = []
  prev = -1
  for p in prices:
    if prev > -1:
      changeSequence.append(p - prev)
    prev = p
  return changeSequence

def processBuyers(buyers):
  processedBuyers = []
  for buyer in buyers:
    processedBuyers.append([buyer, pricesToChangeSequence(buyer)])
  return processedBuyers

def isSameSequence(seq1, seq2):
  for i in range(len(seq1)):
    if not seq1[i] == seq2[i]:
      return False
  debug(f"{seq1} = {seq2}")
  return True

def firstOccurence(sequence, buyer):
  # 0-> prices, 1-> changes
  for i in range(4, 1+len(buyer[1])):
    if isSameSequence(sequence, buyer[1][i-4:i]):
      return buyer[0][i]
  return 0

def countBananas(sequence, buyers):
  bananas = 0
  for i, buyer in enumerate(buyers):
    price = firstOccurence(sequence, buyer)
    debug(f"Got {price} from buyer {i}")
    bananas += price
  return bananas

def fixPrices(buyers):
  fixedPrices = []
  for buyer in buyers:
    fixed = []
    for price in buyer:
      fixed.append(price % 10)
    fixedPrices.append(fixed)
  return fixedPrices

def parseSequence(buyers, strOfSeq):
  for buyer in buyers:
    for i in range(4, 1+len(buyer[1])):
      newStrOfSeq = str(buyer[1][i-4:i])
      if newStrOfSeq == strOfSeq:
        return buyer[1][i-4:i]
  print("Oops")
  return None


def observeSequences(buyers):
  bananasBySeq = {}
  sequencePerBuyer = {}
  #bananasBySeq[str([1,1,1,1])] = 9
  for b, buyer in enumerate(buyers):
    sequencePerBuyer[b] = []
    for i in range(4, 1+len(buyer[1])):
      seq = str(buyer[1][i-4:i])
      if seq in sequencePerBuyer[b]:
        continue #process only first occurence of seq per buyer!
      price = buyer[0][i]
      debug(f"Storing {price} for {seq}")
      if not seq in bananasBySeq:
        bananasBySeq[seq] = price
      else:
        bananasBySeq[seq] += price
      sequencePerBuyer[b].append(seq)

  return bananasBySeq

def pickBestSequence(bananasBySeq):
  bestSeq = None
  bestCount = -1
  for seq in bananasBySeq.keys():
    debug(f"Checking {seq}: {bananasBySeq[seq]}")
    if bananasBySeq[seq] > bestCount:
      bestCount = bananasBySeq[seq]
      bestSeq = seq
  print(f"Best sequence: {bestSeq} yields {bestCount}")
  return bestSeq


def part1(useRealData):
  print("Day " + DAY + ", Part 1")

  input = fetchData(DAY, useRealData)
  initialPrices = transform(input)

  prices = computePrices(initialPrices, 2000)

  sum = sumUp(prices)

  print(f"Result for part 1: {str(sum)}")
  print(f"Expected:          {37327623}")
  if DEBUG:
    initialPrices = [123]
    prices = computePrices(initialPrices, 10)
    print(f"Prices:       {prices}")
    print(f"Expected: '0': [123, 15887950, 16495136, 527345, 704524, 1553684, 12683156, 11100544, 12249484, 7753432, 5908254]")

    nextNumber(1)

def part2(useRealData):
  print("Day " + DAY + ", Part 2")

  input = fetchData(DAY, useRealData)
  initialPrices = transform(input)

  prices = computePrices(initialPrices, 1999)
  fixedPrices = fixPrices(prices)

  buyers = processBuyers(fixedPrices)

  debug(f"{buyers}")

  #sequence = [+1, 1, -1, 5]#findBestSequence(buyers)

  bananasBySeq = observeSequences(buyers)
  strOfSequence = pickBestSequence(bananasBySeq)
  sequence = parseSequence(buyers, strOfSequence)

  bananas = countBananas(sequence, buyers)

  print(f"I got {bananas} for sequence {sequence}")

  if True and DEBUG:
    initialPrices = [1, 2, 3, 2024]
    prices = computePrices(initialPrices, 1999)
    fixedPrices = fixPrices(prices)

    buyers = processBuyers(fixedPrices)

    debug(f"{buyers}")

    bananasBySeq = observeSequences(buyers)
    strOfSequence = pickBestSequence(bananasBySeq)
    sequence = parseSequence(buyers, strOfSequence)

    #sequence = [-2, 1, -1, 3]#findBestSequence(buyers)
    bananas = countBananas(sequence, buyers)

    print(f"I got {bananas} for sequence {sequence}")
    print(f"Best: 23 for sequence [-2, 1, -1, 3]")

def solve():
  #part1(True)
  part2(True)