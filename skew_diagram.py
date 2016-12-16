def minimumSkew(dna):
    skew = [0]
    for i in range(len(dna)):
        if dna[i] == "G":
            skew.append(skew[i] + 1)
        elif dna[i] == "C":
            skew.append(skew[i] - 1)
        else:
            skew.append(skew[i])
    first = min(skew)
    mins = []
    for j in range(len(skew)):
        if skew[j] == first:
            mins.append(j)
#    mins = [i for i, x in enumerate(skew) if x == min(skew)]
    s = " ".join(str(e) for e in mins)
    return s


def findHammingDistance(str1, str2):
    counter = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            counter += 1
    return counter


def findApproximateMatching(dna, kmer, d):
    indices = []
    for i in range(len(dna) - len(kmer)):
        s = dna[i: i + len(kmer)]
        if findHammingDistance(s, kmer) <= d:
            indices.append(i)
    return indices


def countApproximatePattern(dna, kmer, d):
    counter = 0
    for i in range(len(dna) - len(kmer)):
        s = dna[i: i + len(kmer)]
        if findHammingDistance(s, kmer) <= d:
            counter += 1
    return counter

def findNeighbours(pattern, d):
    if d == 0:
        return pattern
    if len(pattern) == 1:
        return ["A", "C", "G", "T"]
    neighborhood = set()
    suffixNeighbors = findNeighbours(pattern[1:], d)
    for text in suffixNeighbors:
        if findHammingDistance(pattern[1:], text) < d:
            for i in "ACGT":
                neighborhood.add(i + text)
        else:
            neighborhood.add(pattern[0:1] + text)
    return neighborhood

def patternToNumber(pattern):
    if len(pattern) == 0:
        return 0
    symbol = pattern[len(pattern) - 1]
    prefix = pattern[0:len(pattern) - 1]
    return 4*patternToNumber(prefix) + symbolToNumber(symbol)

def symbolToNumber(symbol):
    if symbol == "C":
        return 1
    if symbol == "G":
        return 2
    if symbol == "T":
        return 3
    return 0

def numberToPattern(index, k):
    if k == 1:
        return numberToSymbol(index)
    prefixIndex = index//4
    r = index%4
    symbol = numberToSymbol(r)
    prefixPattern = numberToPattern(prefixIndex, k-1)
    return prefixPattern + symbol

def numberToSymbol(number):
    if number == 0:
        return "A"
    if number == 1:
        return "C"
    if number == 2:
        return "G"
    return "T"

def remove_duplicates(l):
    return list(set(l))

def findFrequentWordWithMismatches(Text, k, d):
    FrequentPatterns = set()
    Neighborhoods = []
    neighborhoodArray = []
    frequencyArray = []
    close = []
    for i in range(0, pow(4, k) - 1):
        close.append(0)
        frequencyArray.append(0)
    for j in range(len(Text) - k):
        bb = findNeighbours(Text[j:j+k], d)
        c = list(bb)
        for a in c:
            Neighborhoods.append(a)
        for pattern in range(len(Neighborhoods) - 1):
            index = patternToNumber(Neighborhoods[pattern])
            close[index] = 1
    for l in range(0, pow(4, k) - 1):
        if close[l] == 1:
            pattern = numberToPattern(l, k)
            frequencyArray[l] = countApproximatePattern(Text, pattern, d)
    maxCount = max(frequencyArray)
    for m in range(0, pow(4, k) - 1):
        if frequencyArray[m] == maxCount:
            pattern = numberToPattern(m, k)
            FrequentPatterns.add(pattern)
    return FrequentPatterns

def FrequentWordWithMismatches(Text, k, d):
    FrequentPatterns = set()
    Neighborhoods = []
    neighborhoodArray = []
    count = []
    index = []
    for j in range(len(Text) - k + 1):
        bb = findNeighbours(Text[j:j+k], d)
        c = list([bb])
        if len(bb) == 1:
            Neighborhoods[:0] = [c]
        else:
            for elem in c:
                Neighborhoods.append(elem)
        for p in range(len(Neighborhoods)):
            neighborhoodArray.append(Neighborhoods[p])
    for i in range(len(Neighborhoods)):
        pattern = neighborhoodArray[i]
        index.append(patternToNumber(pattern))
        count.append(1)
    sortedIndex = index[:]
    sortedIndex.sort()
    for l in range(len(Neighborhoods) - 1):
        if sortedIndex[l] == sortedIndex[l+1]:
            count[l+1] = count[l] + 1
    maxCount = max(count)
    for i in range(len(Neighborhoods)):
        if count[i] == maxCount:
            pattern = numberToPattern(sortedIndex[i], k)
            FrequentPatterns.add(pattern)
    return FrequentPatterns
#dna = "AGTCAGCT"
#a = FrequentWordWithMismatches(dna, 4, 2)
#print(len(a))
#print(a)
